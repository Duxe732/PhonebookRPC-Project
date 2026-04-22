import grpc
import phonebook_pb2 as pb
import phonebook_pb2_grpc as pb_grpc
import time


def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = pb_grpc.PhonebookStub(channel)

    print("Welcome to phonebook service!")
    print("Available commands: [Add, Get, Edit, Delete, List]\nTo close the phonebook press Enter")
    action = input("Choose a command: ")
    while action != "":
        try:
            if action == "Add":
                name = input("Enter name: ")
                number = input(f"Enter {name}'s number: ")
                ttl = int(input(f"Enter time to live for {name}'s number: "))
                resp_add = stub.AddEntry(pb.AddRequest(name=name, number=number, ttl_seconds=ttl))
                print(resp_add.message + "\n")
            elif action == "Get":
                name = input("Enter name: ")
                resp_get = stub.GetNumber(pb.GetRequest(name=name))
                print(f"{name}'s number: {resp_get.number}")
            elif action == "Edit":
                name = input("Enter name: ")
                new_number = input("Enter new number or press Enter: ")
                new_ttl = input("Enter new time to live or press Enter: ")
                resp_edit = None
                if new_number != "":
                    if new_ttl != "":
                        resp_edit = stub.EditEntry(pb.EditRequest(name=name, new_number=new_number,
                                                                  new_ttl_seconds=int(new_ttl)))
                    else:
                        resp_edit = stub.EditEntry(pb.EditRequest(name=name, new_number=new_number))
                else:
                    if new_ttl != "":
                        resp_edit = stub.EditEntry(pb.EditRequest(name=name, new_ttl_seconds=int(new_ttl)))
                    else:
                        print("You didn't edit phonebook")
                print(resp_edit.message if resp_edit is not None else print("\n"))
            elif action == "Delete":
                name = input("Enter name: ")
                resp_del = stub.DeleteEntry(pb.DeleteRequest(name=name))
                if resp_del.success:
                    print(f"{name}'s number deleted")
            elif action == "List":
                print("List of all entries", end="")
                resp_list = stub.ListEntries(pb.ListEntriesRequest())
                if not resp_list.entries:
                    print(" is empty")
                else:
                    print(":\n")
                for en in resp_list.entries:
                    print(f"Name: {en.name}, \tNumber: {en.number}, \tExpires at: {time.ctime(en.expires_at)}")
            else:
                print("Choose valid command from [Add, Get, Edit, Delete, List]: ", end="")
            action = input("\nChoose next command: ")
        except grpc.RpcError as e:
            print(f"Error occured: {e.details()}")
            continue


if __name__ == '__main__':
    run()
