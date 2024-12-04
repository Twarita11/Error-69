// Generate Alphabet Buttons Dynamically
const lettersContainer = document.querySelector('.letters-container');
for (let i = 0; i < 26; i++) {
    const letter = String.fromCharCode(65 + i); // Convert ASCII to letters (A-Z)
    const button = document.createElement('button');
    button.classList.add('letter');
    button.setAttribute('data-letter', letter);
    button.innerText = letter;
    lettersContainer.appendChild(button);
}

// Add Click Event for Pronunciation of Letters
document.querySelectorAll('.letter').forEach(button => {
    button.addEventListener('click', () => {
        const letter = button.getAttribute('data-letter');
        readAloud(letter);
    });
});

// Generate Simple Words Dynamically
const wordsContainer = document.querySelector('.words-container');
const words = ['cat', 'dog', 'ball', 'bat', 'apple', 'egg', 'fish', 'goat'];

words.forEach(word => {
    const button = document.createElement('button');
    button.classList.add('word');
    button.setAttribute('data-word', word);
    button.innerText = word;
    wordsContainer.appendChild(button);
});

// Add Click Event for Pronunciation of Words
document.querySelectorAll('.word').forEach(button => {
    button.addEventListener('click', () => {
        const word = button.getAttribute('data-word');
        readAloud(word);
    });
});

// Function to Pronounce Using SpeechSynthesis API
function readAloud(text) {
    const synth = window.speechSynthesis;
    const utterance = new SpeechSynthesisUtterance(text);

    // Optional: Adjust settings for clarity
    utterance.rate = 0.8;
    utterance.pitch = 1.2;

    synth.speak(utterance);
}
