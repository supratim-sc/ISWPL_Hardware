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

// Set checkbox state on load
check_whatsapp_as_phone.checked = whatsapp_number.value === phone_number.value;

// Checkbox logic for syncing WhatsApp with Phone
check_whatsapp_as_phone.addEventListener("change", function () {
  whatsapp_number.value = this.checked ? phone_number.value : "";
});

// Helper function to update reference type related UI
function updateReferenceUI() {
  const selectedText =
    reference_type.options[reference_type.selectedIndex].text.toLowerCase();

  const isTeleCaller = selectedText.startsWith("tele");
  tele_caller_div.style.display = isTeleCaller ? "block" : "none";
  tele_caller_name_input.required = isTeleCaller;

  const isCustomerReference = selectedText === "customer reference";
  customer_reference_div.style.display = isCustomerReference ? "block" : "none";
  customer_reference_name_input.required = isCustomerReference;
}

// Attach event listener and call once on page load
reference_type.addEventListener("change", updateReferenceUI);
updateReferenceUI();
