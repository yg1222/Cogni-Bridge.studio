// Google tracking
// Initializing
window.dataLayer = window.dataLayer || [];
function gtag() { dataLayer.push(arguments); }
gtag('js', new Date());
gtag('config', 'AW-16640354062');

// <!-- Event snippet for Purchase conversion page
// In your html page, add the snippet and call gtag_report_conversion when someone clicks on the chosen link or button. -->
function generateUniqueID() {
   // Generates unique IDs
   return Date.now() + '-' + Math.floor(Math.random() * 1000000);
}

function gtag_report_conversion() {
   try {
      let transactionId = generateUniqueID();
      gtag('event', 'conversion', {
         'send_to': 'AW-16640354062/odkACNyF4MEZEI7O3v49',
         'value': 5.0,
         'currency': 'CAD',
         'transaction_id': transactionId
      });
      return false;
   }
   catch (error) {
      console.error(error)
   }
}


const serverUrl = window.location.origin

// Install buttons on pages with install buttons will have the install-btn as id
// redirect on install click
try {
   document.getElementById('install-btn').addEventListener('click', () => {
      let installUrl = "https://auth.monday.com/oauth2/authorize?client_id=787e3a73ab310b94ea08b147d12dfb57&response_type=install";
      window.open(installUrl, '_blank');
   });
   // google tracking on install click
   document.getElementById('install-btn').addEventListener('click', () => {
      if (window.location.hostname === 'cogni-bridge.studio') {
         gtag_report_conversion()
      }
   });
} catch (e) { console.error(e) }

// Theme code -- end
if (window.location.pathname == "/") {
   document.getElementById('send_btn').addEventListener('click', (e) => {
      e.preventDefault()
      console.log("clicked btn")
      const url = "https://cb-server-production.up.railway.app/contact_messages"
      var msgResponse = document.getElementById('message_response');
      var senderName = document.getElementById('sender-name');
      var senderEmail = document.getElementById('sender-email');
      var senderMessage = document.getElementById('sender-message');
      sendData = {
         "name": senderName.value,
         "email": senderEmail.value,
         "message": senderMessage.value,
         "message_type": "contact_form"
      }
      const opt = {
         method: 'POST',
         headers: {
            'Content-Type': 'application/json',
         },
         body: JSON.stringify(sendData)
      };
      fetch(url, opt)
         .then(res => res.json())
         .then(data => {
            console.log(data)
            if (data.message == "success") {
               console.log("Success response")
               msgResponse.innerText = "Success";
               senderName.innerText = "";
               senderEmail.innerText = "";
               senderMessage.innerText = "";
               // Send email via API
               console.log(serverUrl)
               let notifyOpt = {
                  method: 'POST',
                  headers: {
                     'Content-Type': 'application/json',
                  },
                  body: JSON.stringify({
                     "sender_name": senderName.value,
                     "sender_email": senderEmail.value,
                     "sender_message": senderMessage.value
                  })
               };
               fetch(serverUrl + '/email_notify', notifyOpt).then(res => {
                  // console.log(res.status)
                  if (res.status == 200) {
                     document.getElementById('contact-section').innerHTML = '<h3 class="work_taital">Thank you. Your message was received.</h3>';
                  }
               })
            }
         })
         .catch(error => {
            msgResponse.value = "Error";
         })
   });
}

// Doc2Board page
if (window.location.pathname === "/doc2board") {
   document.getElementById('header-logo').style.maxWidth = '35%';
}


// Doc2board pricing page
const pricingToggle = document.getElementById('pricing-toggle');
const proPrice = document.querySelector('.pro-price');
const unlimitedPrice = document.querySelector('.unlimited-price');

pricingToggle.addEventListener('change', () => {
   if (pricingToggle.checked) {
      proPrice.textContent = '$14';
      unlimitedPrice.textContent = '$54';
   } else {
      proPrice.textContent = '$19';
      unlimitedPrice.textContent = '$59';
   }
});