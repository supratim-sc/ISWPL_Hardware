const phone_number = document.querySelector("#id_phone_number");

const whatsapp_number = document.querySelector("#id_whatsapp_number");
const check_whatsapp_as_phone = document.querySelector(
  "#check_whatsapp_as_phone"
);

const reference_type = document.querySelector("#id_reference_type");
const customer_reference_div = document.querySelector(
  "#customer_reference_div"
);
const customer_reference_name_input = document.querySelector(
  "#id_customer_reference_name"
);
const tele_caller_div = document.querySelector("#tele_caller_div");
const tele_caller_name_input = document.querySelector("#id_tele_caller_name");

// Phone and Whatsapp Number Same or not checkbox logic
check_whatsapp_as_phone.addEventListener("change", function () {
  if (this.checked) {
    whatsapp_number.value = phone_number.value;
  } else {
    whatsapp_number.value = "";
  }
});

// Showing/Hiding Tele Caller name input box depending on reference type
reference_type.addEventListener("change", function () {
  if (
    reference_type.options[reference_type.selectedIndex].text
      .toLowerCase()
      .startsWith("tele")
  ) {
    tele_caller_div.style.display = "block"; // Show the div
    tele_caller_name_input.required = true;
  } else {
    tele_caller_div.style.display = "none"; // Hide the div
    tele_caller_name_input.required = false;
  }
});

// Showing/Hiding Reference Customer inputs depending on reference type
reference_type.addEventListener("change", function () {
  if (
    reference_type.options[reference_type.selectedIndex].text.toLowerCase() ===
    "customer reference"
  ) {
    customer_reference_div.style.display = "block"; // Show customer reference the div
    customer_reference_name_input.required = true;
  } else {
    customer_reference_div.style.display = "none"; // Hide customer refrence the div
    customer_reference_name_input.required = false;
  }
});
