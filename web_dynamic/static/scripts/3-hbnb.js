$(document).ready(function () {
  const AmenitiesChecked = {};
  $(document).on('change', "#select_amenity", function () {
    if (this.checked) {
      AmenitiesChecked[$(this).attr('data-id')] = $(this).attr('data-name');
    } else {
      delete AmenitiesChecked[$(this).attr('data-id')];
    }
    const Firstobj = Object.values(AmenitiesChecked);
    if (Firstobj.length > 3) {
      $('#filter_amen_list').text(Firstobj.sort().slice(0, 3).join(', ') + "...");
    } else if (Firstobj.length <= 3) {
      $('#filter_amen_list').text(Firstobj.sort().join(', '));
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

  $.ajax({
    url: "http://127.0.0.1:5001/api/v1/places_search/",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify({}),
    success: data => {
      for (const place of data.sort()) {
        let article = $('<article></article>');
        article.html(`
          <div class="header_place">
            <div class="place_name"><h2>${ place.name }</h2></div>
            <div class="price_by_night"><p>$${ place.price_by_night }</p></div>
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
            <p><b>Owner:</b> User</p>
          </div>
          <div class="description">
            <p>
              text
            </p>
          </div>
          <div class="amenities">
            <h2>Amenities</h2>
            <ul>
              <li><p>amenity</p></li>
            </ul>
          </div>
          <div class="reviews">
            <h2>Reviews</h2>
            <ul>
              <li>
                <h3>From user the date at hour:</h3>
                <p>
                  text
                </p>
              </li>
            </ul>
          </div>`);
        $('section.places').append(article);
      }
    }
  });
});

