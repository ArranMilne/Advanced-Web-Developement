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






//my code which runs when the 'delete' button is clicked on a flashcard.
document.querySelectorAll('.deleteFlashcardButton').forEach(button => {

    button.addEventListener("click", function() {

    //for the specific flash card clicked, getting it's id value by looking at the id of the object passed to the button. Then I am storing it in a variable to use
    //in the next line
    var specificCardId = this.getAttribute('data-id');
    //using the flashcard id to get the actual flashcard object so the code can delete it.	    
    var flashcard = document.getElementById(`flashcard-${specificCardId}`);


    //removing the specific flashcard
    flashcard.remove();
           
    //addign the flashcards id to the request so that it can be used to identify the card to delete from the database.
    fetch(`/deleteFlashcard/${specificCardId}`, {
	    //to send the data to the server so that it can be used for my flashcard deletion
            method: 'POST'
    });
    });
});



	    



