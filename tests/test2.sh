#!/bin/bash

PROTO_FILE="game.proto"
SERVER_FILE="server.py"
CLIENT_FILE="client.py"

cleanup() {
  if ps -p $SERVER_PID >/dev/null 2>&1; then
    echo "Stopping server (PID $SERVER_PID)"
    kill $SERVER_PID
    rm -f tests/TEST2*_OUTPUT
  fi
}

trap cleanup EXIT

echo "[1/4] Starting server"
python3 "$SERVER_FILE" >tests/TEST2d_OUTPUT &
SERVER_PID=$!
sleep 2

if ! ps -p $SERVER_PID >/dev/null; then
  echo "Server failed to start."
  exit 1
fi

echo "[2/4] Starting clients 1 & 2"
python3 "$CLIENT_FILE" <tests/TEST2a_INPUT >tests/TEST2a_OUTPUT &
CLIENT1_PID=$!
python3 "$CLIENT_FILE" <tests/TEST2b_INPUT >tests/TEST2b_OUTPUT &
CLIENT2_PID=$!
wait $CLIENT1_PID
wait $CLIENT2_PID

echo "[3/4] Starting client 3"
python3 "$CLIENT_FILE" <tests/TEST2c_INPUT >tests/TEST2c_OUTPUT
if ! python3 tests/analyze_output.py <tests/TEST2c_OUTPUT; then
  echo "Client 3 got wrong output."
  exit 1
fi
echo "[4/4] Clients completed. Test successful."
