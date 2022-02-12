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
});