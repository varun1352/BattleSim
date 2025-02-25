document.getElementById('start-game').addEventListener('click', () => {
    fetch('/api/start_game', {
      method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
      document.getElementById('player-one-board').textContent = JSON.stringify(data.board_player_one, null, 2);
      document.getElementById('player-two-board').textContent = JSON.stringify(data.board_player_two, null, 2);
      document.getElementById('result-text').textContent = "Game started!";
    })
    .catch(error => console.error('Error:', error));
  });
  
  document.getElementById('make-move').addEventListener('click', () => {
    const player = document.getElementById('player-select').value;
    const move = document.getElementById('move-input').value.trim();
    if (!move) {
      alert("Please enter a move (e.g., B5)");
      return;
    }
    
    fetch('/api/move', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ player, move })
    })
    .then(response => response.json())
    .then(data => {
      document.getElementById('result-text').textContent = 
        `Move ${data.move}: ${data.result}. Win: ${data.win}`;
      // Update the board display based on the opponent board returned
      if (player === "player_one") {
        document.getElementById('board-player-two').textContent = JSON.stringify(data.opponent_board, null, 2);
      } else {
        document.getElementById('board-player-one').textContent = JSON.stringify(data.opponent_board, null, 2);
      }
    })
    .catch(error => console.error('Error:', error));
  });
  
  document.getElementById('simulate-game').addEventListener('click', () => {
    fetch('/api/simulate')
    .then(response => response.json())
    .then(data => {
      document.getElementById('result-text').textContent = data.prediction;
    })
    .catch(error => console.error('Error:', error));
  });
  