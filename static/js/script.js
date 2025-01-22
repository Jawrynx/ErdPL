const menuToggle = document.getElementById('menu-toggle');
const mobileNav = document.getElementById('mobile-nav');
const navBar = document.getElementById('header');

const homeScores = document.getElementsByClassName('home-score');
const awayScores = document.getElementsByClassName('away-score');

for (let i = 0; i < homeScores.length; i++) {
  const homeScore = parseInt(homeScores[i].textContent, 10); 
  const awayScore = parseInt(awayScores[i].textContent, 10); 

  if (homeScore > awayScore) {
    homeScores[i].classList.add('bold'); 
  } else if (awayScore > homeScore) {
    awayScores[i].classList.add('bold'); 
  }
}

menuToggle.addEventListener('click', () => {
    mobileNav.classList.toggle('active');
    navBar.classList.toggle('mobile-active');
});

// For joining teams to prevent error and correctly select the right team

$(document).ready(function(){
    $("#join-link").click(function(){
      $("#join-team-form").toggle();
    });
  
    $("#join-team-form").submit(function(event) {
      event.preventDefault(); 
  
      var selectedTeamId = $("#team_id_select").val(); 
      console.log("Selected Team ID:", selectedTeamId); 
  
      if (selectedTeamId) {
        // No URL construction needed
        var actionUrl = "../../../teams/" + selectedTeamId + "/join/"; 
        $(this).attr('action', actionUrl); 
        this.submit(); 
      } else {
        alert("Please select a team.");
      }
    });
  });


// Create Team Form Validation

const isCaptainInput = document.getElementById('team-captain-input');
const teamSubmitButton = document.getElementById('team-submit-button');
const notCaptainError = document.getElementById('team-form-error-message');

isCaptainInput.addEventListener('change', () => {
  if (!isCaptainInput.checked) {
    notCaptainError.classList.remove('hidden'); 
    teamSubmitButton.classList.add('hidden'); 
  } else {
    notCaptainError.classList.add('hidden'); 
    teamSubmitButton.classList.remove('hidden'); 
  }
});