$(document).ready(function () {

  const AmenitiesChecked = {};
  $(document).on('change', "#select_amenity", function () {
    if (this.checked) {
      AmenitiesChecked[$(this).attr('data-id')] = $(this).attr('data-name');
    } else {
      delete AmenitiesChecked[$(this).attr('data-id')];
    }
    const Firstobj = Object.values(AmenitiesChecked);
    console.log(Firstobj);
    if (Firstobj.length > 3) {
      $('#filter_amen_list').text(Firstobj.sort().slice(0, 3).join(', ') + "...");
    } else if (Firstobj.length <= 3) {
      $('#filter_amen_list').text(Firstobj.sort().join(', '));
    }
  });

  const StatesChecked = {};
  $(document).on('change', "#select_state", function () {
    if (this.checked) {
      StatesChecked[$(this).attr('data-id')] = $(this).attr('data-name');
    } else {
      delete StatesChecked[$(this).attr('data-id')];
    }
    const Firstobj = Object.values(StatesChecked);
    console.log(Firstobj);
    if (Firstobj.length > 3) {
      $('#filter_state_city').text('States: ' + Firstobj.sort().slice(0, 3).join(', ') + "...");
    } else if (Firstobj.length <= 3) {
      $('#filter_state_city').text(Firstobj.sort().join(', '));
    }
  });

  const CitiesChecked = {};
  $(document).on('change', "#select_city", function () {
    if (this.checked) {
      CitiesChecked[$(this).attr('data-id')] = $(this).attr('data-name');
    } else {
      delete CitiesChecked[$(this).attr('data-id')];
    }
    const Firstobj = Object.values(CitiesChecked);
    console.log(Firstobj);
    if (Firstobj.length > 3) {
      $('#filter_state_city').text('Cities: ' + Firstobj.sort().slice(0, 3).join(', ') + "...");
    } else if (Firstobj.length <= 3) {
      $('#filter_state_city').text('Cities: ' + Firstobj.sort().join(', '));
    }
  });

  $.getJSON("http://127.0.0.1:5001/api/v1/status/",
    function (data) {
      if (data.status === 'OK') {
        $('div#api_status').addClass('available');
      } else {
        $('div#api_status').removeClass('available');
      }
    }
  );

  const users = {};
  $.getJSON("http://127.0.0.1:5001/api/v1/users/",
    function (data) {
      for (const user of data) {
        users[user.id] = user.first_name + " " + user.last_name;
      }
    }
  );

  let dictusers = {};
  $.getJSON("http://127.0.0.1:5001/api/v1/users/",
    function (data) {
      for (user of data) {
        dictusers[user.id] = user.first_name + " " + user.last_name;
      }
    }
  );

  function show_places (amenities, states, cities) {
    let am = {};
    let st = {};
    let ct = {};
    if (amenities !== undefined) {
      let am_ids = [];
      for (const id in amenities) {
        am_ids.push(id.toString());
      }
      am = {'amenities': am_ids};
    }
    if (states !== undefined) {
      let st_ids = [];
      for (const id in states) {
        st_ids.push(id.toString());
      }
      st = {'states': st_ids};
    }
    if (cities !== undefined) {
      let ct_ids = [];
      for (const id in cities) {
        ct_ids.push(id.toString());
      }
      ct = {'cities': ct_ids};
    }
    const filters = {'filters': [am, st, ct]}
    $.ajax({
      url: "http://127.0.0.1:5001/api/v1/places_search/",
      type: "POST",
      contentType: "application/json",
      data: JSON.stringify(filters),
      success: function (data) {
        $('section.places').html('');
        for (const place of data) {
          let dictamenities = {};
          $.getJSON("http://127.0.0.1:5001/api/v1/places/" + place.id + "/amenities",
            function (data) {
              for (amens of data) {
                dictamenities[amens.id] = amens.name;
              }
            }
          )

          let dictreviews = {};
          $.getJSON("http://127.0.0.1:5001/api/v1/places/" + place.id + "/reviews",
            function (data) {
              for (revw of data) {
                dictreviews[revw.user_id] = {};
                dictreviews[revw.user_id]['name'] = dictusers[revw.user_id];
                dictreviews[revw.user_id]['date'] = revw.created_at;
                dictreviews[revw.user_id]['text'] = revw.text;
              }
            }
          );

          let lstamenities = $("<ul></ul>");
          for (amens in dictamenities) {
            lstamenities.append(`<li><p>${ dictamenities[amens] }</p></li>`);
          }

           let lstreviews = $("<ul id='HTMLreview'></ul>");
           for (revw in dictreviews) {
            lstreviews.append(`
              <li>
                <h3>From ${ dictreviews[revw]['name'] } the ${ dictreviews[revw]['date'] }:</h3>
                <p>
                  ${ dictreviews[revw]['text'] }
                </p>
              </li>`);
            }
          
          console.log(lstamenities); 
          console.log(lstreviews);


          let article = $('<article></article>');
          article.html(`
            <div class="header_place">
              <div class="place_name"><h2>${ place.name }</h2></div>
              <div class="price_by_night">
                <p>$${ place.price_by_night }</p>
              </div>
            </div>
            <div class="information">
              <div class="max_guest">
                <div class="img"></div>
                <p>${ place.max_guest } Guest(s)</p>
              </div>
              <div class="number_rooms">
                <div class="img"></div>
                <p>${ place.number_rooms } Bedroom(s)</p>
              </div>
              <div class="number_bathrooms">
                <div class="img"></div>
                <p>${ place.number_bathrooms } Bathroom(s)</p>
              </div>
            </div>
            <div class="user">
              <p><b>Owner:</b> ${ users[place.user_id] }</p>
            </div>
            <div class="description">
              <p>
                ${ place.description }
              </p>
            </div>
            <div class="amenities">
              <h2>Amenities</h2>
              ${ lstamenities.html() }
            </div>
            <div class="reviews">
              <h2>Reviews</h2>
              ${ lstreviews.html() }
            </div>`);
          $('section.places').append(article);
        }
      }
    });
  }

  show_places();

  $('button#bt_search').click(function () {
    show_places(AmenitiesChecked, StatesChecked, CitiesChecked);
  });

});

