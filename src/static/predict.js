document.addEventListener('DOMContentLoaded', onLoad);

function onLoad(){
  console.log("DOM loaded");

  const leagueSelect = document.getElementById('league_select');

  fetch('/api/all_leagues')
    .then(response => response.json())
    .then(data => {
        // Trabaja con los datos recibidos y rellena el select
        const select = document.getElementById('league_select');

        data.leagues.forEach(league => {
            const option = document.createElement('option');
            option.value = league.strLeague;
            option.text = league.strLeague;
            select.add(option);
        });
        getTeams(leagueSelect.value)
    })
    .catch(error => {
        // Manejar errores
        console.error('Error en la petición:', error);
    });




  // Añade un evento 'change' al select
  leagueSelect.addEventListener('change', function() {
    getTeams(leagueSelect.value)
  });

  document.getElementById("predict").addEventListener("click", onPredict)
}


function getTeams(name){
  // Obtén los datos de los equipos
fetch(`/api/teams_by_league?name=${name}`)
.then(response => {
  if (!response.ok) {
    throw new Error('Error en la solicitud a la API');
  }
  return response.json();
})
.then(data => {
  // Obtén las referencias a los elementos select
  const teamHomeSelect = document.getElementById('team_home_select');
  const teamVisitorSelect = document.getElementById('team_visitor_select');

  // Limpia cualquier opción existente en los select
  teamHomeSelect.innerHTML = '';
  teamVisitorSelect.innerHTML = '';

  // Rellena los select con los nombres de los equipos
  data.teams.forEach(team => {
    const optionHome = document.createElement('option');
    optionHome.value = team.idTeam;
    optionHome.text = team.strTeam;
    teamHomeSelect.add(optionHome);

    const optionVisitor = document.createElement('option');
    optionVisitor.value = team.idTeam;
    optionVisitor.text = team.strTeam;
    teamVisitorSelect.add(optionVisitor);
  });
})
.catch(error => {
  // Manejar errores
  console.error('Error en la petición:', error);
});
}


function onPredict(){
  let home_team = document.getElementById("team_home_select").value
  let visitor_team = document.getElementById("team_visitor_select").value
  let date = document.getElementById("date").value;
  let time = document.getElementById("time").value;

  console.log("Predict " + home_team + " vs " + visitor_team + " on " + date + " at " + time);
}