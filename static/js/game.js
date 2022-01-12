const gameId = JSON.parse(document.getElementById("game_id").textContent);
let userId;
let userNumber;
let myTurn = false;

// functions
const showWaitingUI = () => {
  document.getElementById("loading-ui").style.display = "none";
  document.getElementById("game-ui").style.display = "none";
  document.getElementById("waiting-ui").style.display = "block";
};
const showGameUI = () => {
  document.getElementById("loading-ui").style.display = "none";
  document.getElementById("waiting-ui").style.display = "none";
  document.getElementById("game-ui").style.display = "block";
};

// link text shown and copy link
document.getElementById("linkText").value = location.href;
const copyLink = () => {
  let copyText = document.getElementById("linkText");
  copyText.select();
  copyText.setSelectionRange(0, 99999); /* For mobile devices */

  /* Copy the text inside the text field */
  navigator.clipboard.writeText(copyText.value);
  document.getElementById("copyButton").title = "Copied";
  document.getElementById(
    "copyButton"
  ).innerHTML = `<i class="bi bi-clipboard-check"></i>`;
  setTimeout(() => {
    document.getElementById(
      "copyButton"
    ).innerHTML = `<i class="bi bi-clipboard"></i>`;
    document.getElementById("copyButton").title = "Copy";
  }, 5000);
};

const freshResult = () => {
  document.getElementById("opponent-done").style.display = "none";
  document.getElementById("opponent-choice").style.display = "none";
  document.getElementById("opponent-loading").style.display = "block";
  myTurn = true;
  document.querySelectorAll(".choice").forEach((ele) => {
    ele.style.display = "block";
  });
};

const showResult = (winner, yourChoice, opponentChoice) => {
  document.getElementById(
    "opponent-image"
  ).src = `/static/images/${opponentChoice}.png`;

  document.getElementById("opponent-done").style.display = "none";
  document.getElementById("opponent-loading").style.display = "none";
  document.getElementById("opponent-choice").style.display = "block";

  setTimeout(() => {
    if (winner === null) {
      swal({
        title: "No one wins",
        text: "It was a tie.",
        icon: "info",
      });
    } else if (winner === userId) {
      swal({
        title: "Hoorah!",
        text: "You win the match",
        icon: "success",
      });
    } else {
      swal({
        title: "Oops!",
        text: "You lost the match",
        icon: "error",
      });
    }
    freshResult();
  }, 1500);
};

// construct websoket
const client = new WebSocket(`ws://${location.host}/ws/game/${gameId}/`);

client.onopen = (e) => {
  console.log("Websocket Connected!");
};

client.onmessage = (e) => {
  let data = JSON.parse(e.data);
  switch (data.type) {
    case "waiting":
      userId = data.userId;
      userNumber = 1;
      showWaitingUI();
      break;
    case "startGame":
      if (userNumber !== 1) {
        userNumber = 2;
        userId = data.userId;
      }
      showGameUI();
      myTurn = true;
      break;
    case "played":
      if (data.userId !== userId) {
        document.getElementById("opponent-loading").style.display = "none";
        document.getElementById("opponent-choice").style.display = "none";
        document.getElementById("opponent-done").style.display = "block";
      }
      break;
    case "result":
      let yourChoice, opponentChoice, yourScore, opponentScore;
      if (userNumber === 1) {
        yourChoice = data.user1Choice;
        opponentChoice = data.user2Choice;
        yourScore = data.user1Score;
        opponentScore = data.user2Score;
      } else {
        yourChoice = data.user2Choice;
        opponentChoice = data.user1Choice;
        yourScore = data.user2Score;
        opponentScore = data.user1Score;
      }
      showResult(data.winner, yourChoice, opponentChoice);
      // update score and round number
      let currentRound = data.currentRound + 1;
      document.getElementById("round-number").textContent = currentRound;
      document.getElementById("your-score").textContent = yourScore;
      document.getElementById("opponent-score").textContent = opponentScore;

      break;
    case "deleteRoom":
      alert("You opponent leave the game.");
      location.href = location.origin;
      break;
    default:
      console.log(data);
  }
};

client.onclose = (e) => {
  console.log("Websocket Closed!");
};
client.onerror = (e) => {
  console.log(e);
};

// choice select
document.querySelectorAll(".choice").forEach((ele) => {
  ele.addEventListener("click", (e) => {
    if (myTurn) {
      // hide all picture rather than answer
      document.querySelectorAll(".choice").forEach((ele) => {
        ele.style.display = "none";
      });
      e.target.style.display = "block";
      let turn = e.target.dataset.item;
      // send answer
      client.send(
        JSON.stringify({
          type: "saveTurn",
          turn,
          userId,
        })
      );
      myTurn = false;
    }
  });
});

// enable tooltip
var tooltipTriggerList = [].slice.call(
  document.querySelectorAll('[data-bs-toggle="tooltip"]')
);
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl);
});
