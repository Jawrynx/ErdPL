const menuToggle = document.getElementById('menu-toggle');
const mobileNav = document.getElementById('mobile-nav');
const navBar = document.getElementById('header');


menuToggle.addEventListener('click', () => {
    mobileNav.classList.toggle('active');
    navBar.classList.toggle('mobile-active');
});

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