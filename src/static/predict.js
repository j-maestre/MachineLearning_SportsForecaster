document.addEventListener('DOMContentLoaded', onLoad);


let match_info = {
  home_team : String,
  visitor_team : String,
  home_goals : Number,
  visitor_goals : Number,
  home_posesion: Number,
  visitor_posesion: Number,
};


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
    optionHome.id = team.strTeam;
    teamHomeSelect.add(optionHome);

    const optionVisitor = document.createElement('option');
    optionVisitor.value = team.idTeam;
    optionVisitor.text = team.strTeam;
    optionVisitor.id = team.strTeam;
    teamVisitorSelect.add(optionVisitor);
  });
})
.catch(error => {
  // Manejar errores
  console.error('Error en la petición:', error);
});
}


function onPredict(){
  let home = document.getElementById("team_home_select");
  let visitor = document.getElementById("team_visitor_select");
  
  let home_team = home.value
  let visitor_team = visitor.value

  let home_name = home.options[home.selectedIndex].id;
  let visitor_name = visitor.options[visitor.selectedIndex].id;


  let date = document.getElementById("date").value;
  let time = document.getElementById("time").value;

  console.log("Predict " + home_name + home_team + " vs " + visitor_name + visitor_team + " on " + date + " at " + time);

  fetch(`/api/get?id_team=${home_team}`)
  .then(response => {
    if (!response.ok) {
      throw new Error('Error en la solicitud a la API');
    }
    return response.json();
  })
  .then(data => {

    console.log("----- Last 5 events home playing at home -----")
    // Rellena los select con los nombres de los equipos
    data.results.forEach(team => {
      console.log(team.strHomeTeam + " " + team.intHomeScore + " - " + team.intAwayScore + " " + team.strAwayTeam);  
    });
    console.log("----- -----")
    
    //console.log(data)
  })
  .catch(error => {
    // Manejar errores
    console.error('Error en la petición:', error);
  });


  let match_info_list = [];
  console.log(home_name + " vs " + visitor_name)

  fetch(`/api/get/team_vs_team?id_team_first=${home_name}&id_team_second=${visitor_name}`).then(response => {
    if (!response.ok) {
      throw new Error('Error en la solicitud a la API');
    }
    return response.json();
  }).then(data => {


    console.log("----- Last events "+home_name+" vs "+visitor_name+" -----")
    // Rellena los select con los nombres de los equipos
    data.event.forEach(event => {
      console.log(event)
      let match = {
        home_team : home_name,
        visitor_team : visitor_name,
        home_goals : event.intHomeScore,
        visitor_goals : event.intAwayScore,
      };

      if(event.intHomeScore != null && event.intAwayScore != null){
        match_info_list.push(match);
      }

      //console.log(event.strHomeTeam + " " + event.intHomeScore + " - " + event.intAwayScore + " " + event.strAwayTeam);
      
    });
    console.log(match_info_list)
    console.log("----- -----")

    


    train_neural(match_info_list)
    // mostrar_resultados_team me devuelve los ultimos 5 partidos de un equipo en casa
    
  }).catch(error => {
    // Manejar errores
    console.error('Error en la petición:', error);
  });

  console.log("Fuera del bicho");


  //train_neural(match_info_list)


  // Coger todos los datos posibles de home_team vs visitor_team
  // En el free solo se puede los ultimos partidos locales, asi que de momento hay que coger los ultimos partidos de home_team

}

async function GetLastFive(name){

  fetch(`/liga/<name>/<id_team>`).then(response => {
    if (!response.ok) {
      throw new Error('Error en la solicitud a la API');
    }
    return response.json();
  }).then(data => {


    console.log("----- Last events "+home_name+" vs "+visitor_name+" -----")
    // Rellena los select con los nombres de los equipos
    data.event.forEach(event => {
      console.log(event)
      let match = {
        home_team : home_name,
        visitor_team : visitor_name,
        home_goals : event.intHomeScore,
        visitor_goals : event.intAwayScore,
      };

      if(event.intHomeScore != null && event.intAwayScore != null){
        match_info_list.push(match);
      }

      //console.log(event.strHomeTeam + " " + event.intHomeScore + " - " + event.intAwayScore + " " + event.strAwayTeam);
      
    });
    console.log(match_info_list)
    console.log("----- -----")

    


    train_neural(match_info_list)

    

    // mostrar_resultados_team me devuelve los ultimos 5 partidos de un equipo en casa
    
  }).catch(error => {
    // Manejar errores
    console.error('Error en la petición:', error);
  });
}



function train_neural(data){
  console.log("Training neural")

  data_raw = encodeURIComponent(JSON.stringify(data))

  fetch(`/api/train?data=${data_raw}`).then(response => {
    if (!response.ok) {
      throw new Error('Error en la solicitud a la API');
    }
    return response.json();
  }).then(data => {

    console.log("Entrenamiento finalizado");
    console.log(data.home_team + " " + data.predicted_home_goals + " - " + data.predicted_visitor_goals + " " + data.visitor_team);

    document.getElementById("predict_result").innerHTML = `${data.home_team} ${data.predicted_home_goals.toFixed(2)} - ${data.predicted_visitor_goals.toFixed(2)} ${data.visitor_team}`;

  }).catch(error => {
    // Manejar errores
    console.error('Error en la petición:', error);
  });
    
  
}