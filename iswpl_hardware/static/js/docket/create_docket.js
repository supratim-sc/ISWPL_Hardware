const phone_number = document.querySelector("#id_phone_number");

const whatsapp_number = document.querySelector("#id_whatsapp_number");
const check_whatsapp_as_phone = document.querySelector(
  "#check_whatsapp_as_phone"
);

whatsapp_number.addEventListener("change", function () {
  if (whatsapp_number.value == phone_number.value) {
    check_whatsapp_as_phone.checked = true;
  } else {
    check_whatsapp_as_phone.checked = false;
  }
});

// Phone and Whatsapp Number Same or not checkbox logic
check_whatsapp_as_phone.addEventListener("change", function () {
  if (this.checked) {
    whatsapp_number.value = phone_number.value;
  } else {
    whatsapp_number.value = "";
  }
});
