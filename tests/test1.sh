#!/bin/bash

PROTO_FILE="game.proto"
SERVER_FILE="server.py"
CLIENT_FILE="client.py"

cleanup() {
  if ps -p $SERVER_PID >/dev/null 2>&1; then
    echo "Stopping server (PID $SERVER_PID)"
    kill $SERVER_PID
  fi
  rm -f tests/TEST1a_OUTPUT tests/TEST1b_OUTPUT
}

trap cleanup EXIT

echo "[1/3] Starting server"
python3 "$SERVER_FILE" &
SERVER_PID=$!
sleep 2

if ! ps -p $SERVER_PID >/dev/null; then
  echo "Server failed to start."
  exit 1
fi

echo "[2/3] Starting clients"
python3 "$CLIENT_FILE" <tests/TEST1a_INPUT >tests/TEST1a_OUTPUT
if ! diff tests/TEST1a_OUTPUT tests/TEST1a_FILE >/dev/null; then
  echo "Client 1 got wrong output."
  exit 1
fi
python3 "$CLIENT_FILE" <tests/TEST1b_INPUT >tests/TEST1b_OUTPUT
if ! diff tests/TEST1b_OUTPUT tests/TEST1b_FILE >/dev/null; then
  echo "Client 2 got wrong output."
  exit 1
fi
echo "[3/3] Clients completed. Test successful."
