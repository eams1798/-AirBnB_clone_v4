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
});