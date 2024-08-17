import React, { useState, useEffect } from 'react';
import { io } from 'socket.io-client';

const socket = io('http://localhost:5555'); // Flask 서버와 WebSocket 연결

function Game() {
  const [roomId, setRoomId] = useState('');
  const [playerId, setPlayerId] = useState('');
  const [guess, setGuess] = useState('');
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    // 서버로부터 메시지를 받을 때 처리하는 로직
    socket.on('player_joined', (data) => {
      setMessages((msgs) => [...msgs, `${data.player_id} joined the game`]);
    });

    socket.on('correct_guess', (data) => {
      setMessages((msgs) => [...msgs, `${data.player_id} guessed the word: ${data.word}`]);
    });

    socket.on('wrong_guess', (data) => {
      setMessages((msgs) => [...msgs, `${data.player_id} guessed wrong: ${data.guess}`]);
    });

    socket.on('next_turn', (data) => {
      setMessages((msgs) => [...msgs, `It's now ${data.next_player}'s turn`]);
    });

    // 컴포넌트가 언마운트될 때 소켓 연결 종료
    return () => {
      socket.disconnect();
    };
  }, []);

  const joinRoom = () => {
    socket.emit('join', { room_id: roomId, player_id: playerId });
  };

  const sendGuess = () => {
    socket.emit('guess', { room_id: roomId, player_id: playerId, guess: guess });
    setGuess('');
  };

  return (
    <div>
      <input 
        type="text" 
        placeholder="Room ID" 
        value={roomId} 
        onChange={(e) => setRoomId(e.target.value)} 
      />
      <input 
        type="text" 
        placeholder="Player ID" 
        value={playerId} 
        onChange={(e) => setPlayerId(e.target.value)} 
      />
      <button onClick={joinRoom}>Join Room</button>

      <div>
        <input 
          type="text" 
          placeholder="Your Guess" 
          value={guess} 
          onChange={(e) => setGuess(e.target.value)} 
        />
        <button onClick={sendGuess}>Submit Guess</button>
      </div>

      <div>
        <h2>Game Messages:</h2>
        <ul>
          {messages.map((msg, index) => (
            <li key={index}>{msg}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Game;
