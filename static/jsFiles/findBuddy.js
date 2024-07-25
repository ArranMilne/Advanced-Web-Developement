


//using 'querySelectorAll' to select all flashcards which have a button with the class called 'showAnswerButton'.

document.querySelectorAll(".showAnswerButton").forEach(button => {

   //adding a click event listener to each button so that it is clickable.
   button.addEventListener("click", function() {

      //for each button, getting the webpage element which is directly before the button. This is the flashcards answer text.
       var answer = this.previousElementSibling;

       //when each button is clicked, the code checks the current value of the text on the button so that it can be swapped to the other.
       this.textContent = this.textContent === "Show Answer" ? "Hide Answer" : "Show Answer";

       //when each button is clicked, my code checks the display property of the answer text so that it can be swapped to visible or non-visible depending on if we want to see the answer.
       answer.style.display = answer.style.display === "none" ? "block" : "none";


    });
});



