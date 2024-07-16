const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const input = document.getElementById('answerInput');
const promptSpan = document.getElementById('prompt');
const finalScoreDiv = document.getElementById('final-score');

let fallingNumber;
let score = 0;
let lives = 3;
let highScore = 0;
let highScoreDate = '';
let gameOver = false;

function getRandomFactor() {
    return Math.floor(Math.random() * 9) + 2;
}

function generateFallingNumber() {
    const factor1 = getRandomFactor();
    const factor2 = getRandomFactor();
    return {
        value: factor1 * factor2,
        factor1,
        factor2,
        x: Math.random() * (canvas.width - 50),
        y: -50,
        speed: 2,
        color: 'black',
        attempts: 0
    };
}

function drawText(text, x, y, color = 'black', fontSize = 30) {
    ctx.fillStyle = color;
    ctx.font = `${fontSize}px Arial`;
    ctx.fillText(text, x, y);
}

function update() {
    if (gameOver) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    fallingNumber.y += fallingNumber.speed;

    drawText(`Vidas: ${lives}`, 10, 30, 'red');
    drawText(`Puntaje: ${score}`, canvas.width - 150, 30, 'red');
    drawText(fallingNumber.value, fallingNumber.x, fallingNumber.y, fallingNumber.color);

    if (fallingNumber.y > canvas.height) {
        lives -= 1;
        if (lives === 0) {
            gameOver = true;
            handleGameOver();
        } else {
            resetFallingNumber();
        }
    }

    requestAnimationFrame(update);
}

function resetFallingNumber() {
    fallingNumber = generateFallingNumber();
    promptSpan.textContent = `${fallingNumber.factor1} x `;
    input.value = '';
}

function handleGameOver() {
    saveHighScore();
    finalScoreDiv.hidden = false;
    finalScoreDiv.innerHTML = `
        <p>Puntaje Final: ${score}</p>
        <p>Puntaje Más Alto: ${highScore} (${highScoreDate})</p>
        <p>Presiona 'R' para volver a jugar o 'ESC' para salir</p>
    `;

    document.addEventListener('keydown', (event) => {
        if (event.key === 'r') {
            finalScoreDiv.hidden = true;
            restartGame();
        } else if (event.key === 'Escape') {
            window.close();
        }
    });
}

function restartGame() {
    score = 0;
    lives = 3;
    gameOver = false;
    resetFallingNumber();
    update();
}

function handleInput(event) {
    if (event.key === 'Enter') {
        const inputValue = input.value.trim();
        const inputFactor2 = parseInt(inputValue);
        if (!isNaN(inputFactor2)) {
            const product = fallingNumber.factor1 * inputFactor2;
            if (product === fallingNumber.value) {
                score += 1;
                resetFallingNumber();
            } else {
                score -= 1;
                fallingNumber.attempts += 1;
                if (fallingNumber.attempts === 1) {
                    fallingNumber.color = 'orange';
                    input.value = '';
                } else if (fallingNumber.attempts === 2) {
                    lives -= 1;
                    if (lives === 0) {
                        gameOver = true;
                        handleGameOver();
                    } else {
                        resetFallingNumber();
                    }
                }
            }
        }
    }
}

function saveHighScore() {
    const date = new Date().toLocaleString();
    if (score > highScore) {
        highScore = score;
        highScoreDate = date;
        localStorage.setItem('highScore', highScore);
        localStorage.setItem('highScoreDate', highScoreDate);
    }
}

function loadHighScore() {
    const savedHighScore = localStorage.getItem('highScore');
    const savedHighScoreDate = localStorage.getItem('highScoreDate');
    if (savedHighScore) {
        highScore = parseInt(savedHighScore);
        highScoreDate = savedHighScoreDate;
    }
}

function init() {
    loadHighScore();
    resetFallingNumber();
    update();
    input.addEventListener('keydown', handleInput);
}

init();
