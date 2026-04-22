import grpc
import time
import threading
from concurrent import futures
import phonebook_pb2 as pb
import phonebook_pb2_grpc as pb_grpc


class Entry:
    def __init__(self, number, expires_at):
        self.number = number
        self.expires_at = expires_at


class PhonebookServicer(pb_grpc.PhonebookServicer):
    def __init__(self):
        self.db = {}
        self.lock = threading.Lock()

    def get_entry(self, name):
        with self.lock:
            entry = self.db.get(name)
            if entry is None:
                return
            if entry.expires_at <= time.time():
                del self.db[name]
                return
            return entry

    def AddEntry(self, request, context):
        print(f"[AddEntry] name={request.name}, number={request.number}, ttl={request.ttl_seconds}")
        if not request.name or not request.number:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "Name and number are required")
        if request.ttl_seconds <= 0:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT, "TTL must be positive")

        expires_at = time.time() + request.ttl_seconds
        entry = Entry(request.number, expires_at)

        with self.lock:
            self.db[request.name] = entry

        return pb.AddResponse(success=True, message="Entry added", name=request.name, number=request.number,
                              expires_at=int(expires_at))

    def GetNumber(self, request, context):
        print(f"[GetNumber] name={request.name}")
        entry = self.get_entry(request.name)
        if entry is None:
            context.abort(grpc.StatusCode.NOT_FOUND, f"Name '{request.name}' not found or expired")
        return pb.GetResponse(number=entry.number, expires_at=int(entry.expires_at))

    def EditEntry(self, request, context):
        print(f"[EditEntry] name={request.name}")
        with self.lock:
            entry = self.db.get(request.name)
            if entry is None:
                context.abort(grpc.StatusCode.NOT_FOUND, f"Name '{request.name}' not found")
            if entry.expires_at <= time.time():
                del self.db[request.name]
                context.abort(grpc.StatusCode.NOT_FOUND, "Entry expired")

            new_number = entry.number
            new_expires = entry.expires_at

            if request.HasField('new_number'):
                self.db[request.name].number = request.new_number
                new_number = request.new_number
            if request.HasField('new_ttl_seconds'):
                if request.new_ttl_seconds <= 0:
                    context.abort(grpc.StatusCode.INVALID_ARGUMENT, "TTL must be positive")
                new_expires = time.time() + request.new_ttl_seconds
                self.db[request.name].expires_at = new_expires
        return pb.EditResponse(success=True, message="Entry updated", new_number=new_number,
                               new_expires_at=int(new_expires))

    def DeleteEntry(self, request, context):
        print(f"[DeleteEntry] name={request.name}")
        with self.lock:
            if request.name in self.db:
                if self.db[request.name].expires_at < time.time():
                    del self.db[request.name]
                    context.abort(grpc.StatusCode.NOT_FOUND, "Entry expired")
                else:
                    del self.db[request.name]
                    return pb.DeleteResponse(success=True)
            else:
                context.abort(grpc.StatusCode.NOT_FOUND, f"Name '{request.name}' not found")

    def ListEntries(self, request, context):
        print(f"[List Entries] request")
        with self.lock:
            valid_db = {}
            entries = []
            for i in self.db:
                if self.db[i].expires_at > time.time():
                    entry = self.db[i]
                    valid_db[i] = entry
                    entries.append(pb.Entry(
                        name=i,
                        number=entry.number,
                        expires_at=int(entry.expires_at)
                    ))
            self.db = valid_db
        return pb.ListEntriesResponse(entries=entries)


def main():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb_grpc.add_PhonebookServicer_to_server(PhonebookServicer(), server)
    server.add_insecure_port('0.0.0.0:50051')
    print("Server listening on 0.0.0.0:50051")
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)
        server.wait_for_termination()
        print("Shutting down...")


if __name__ == '__main__':
    main()
