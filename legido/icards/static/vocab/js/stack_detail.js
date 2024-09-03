// static/icards/stack_detail.js

document.addEventListener('DOMContentLoaded', function () {
    const selectAllCheckbox = document.getElementById('select-all');
    const cardCheckboxes = document.querySelectorAll('.card-checkbox');

    // "Select All" checkbox controls all card checkboxes
    selectAllCheckbox.addEventListener('change', function () {
        const isChecked = selectAllCheckbox.checked;
        cardCheckboxes.forEach(function (checkbox) {
            checkbox.checked = isChecked;
        });
    });

    // If any card checkbox is unchecked, uncheck the "Select All" checkbox
    cardCheckboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            if (!checkbox.checked) {
                selectAllCheckbox.checked = false;
            } else if (Array.from(cardCheckboxes).every((chk) => chk.checked)) {
                // If all checkboxes are checked after this change, check "Select All"
                selectAllCheckbox.checked = true;
            }
        });
    });
});
