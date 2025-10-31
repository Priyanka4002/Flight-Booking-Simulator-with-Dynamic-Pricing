// 🌍 Base URL of your FastAPI backend
const API_BASE = "http://127.0.0.1:8000";

// -----------------------------------------------------
// 🔹 Search Flights (index.html)
// -----------------------------------------------------
async function searchFlights() {
  const origin = document.getElementById("origin").value.trim();
  const destination = document.getElementById("destination").value.trim();
  const departure_time = document.getElementById("departure_time").value;

  if (!origin || !destination) {
    alert("Please enter both origin and destination.");
    return;
  }

  let url = `${API_BASE}/search?origin_city=${origin}&destination_city=${destination}`;
  if (departure_time){
    url += `&departure_time=${departure_time.replace("T", " ")}`;
  }
  try {
    const res = await fetch(url);
    const data = await res.json();

    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    if (!res.ok) {
      resultsDiv.innerHTML = `<p class='error'>${data.detail || "No flights found"}</p>`;
      return;
    }

    if (data.length === 0) {
      resultsDiv.innerHTML = "<p>No flights available for the given criteria.</p>";
      return;
    }

    data.forEach((flight) => {
      const card = document.createElement("div");
      card.className = "flight-card";
      card.innerHTML = `
        <h3>${flight.origin_city} → ${flight.destination_city}</h3>
        <p>✈️ Airline: <b>${flight.operator_name}</b> (${flight.airline_code})</p>
        <p>🕒 Departure: ${flight.departure_time}</p>
        <p>💰 Price: ₹${flight.ticket_price}</p>
        <p>🪑 Seats Left: ${flight.available_seats}</p>
        <button onclick="goToBooking('${flight.airline_code}')">Book Now</button>
      `;
      resultsDiv.appendChild(card);
    });
  } catch (error) {
    console.error("Error fetching flights:", error);
    alert("Failed to connect to the backend server.");
  }
}

// -----------------------------------------------------
// 🔹 Navigate to Booking Page
// -----------------------------------------------------
function goToBooking(airlineCode) {
  localStorage.setItem("selected_airline", airlineCode);
  window.location.href = "booking.html";
}

// -----------------------------------------------------
// 🔹 Booking Page: Autofill selected airline
// -----------------------------------------------------
if (window.location.pathname.includes("booking.html")) {
  const airline = localStorage.getItem("selected_airline");
  if (airline) document.getElementById("airline_code").value = airline;
}

// -----------------------------------------------------
// 🔹 Create Booking (booking.html)
// -----------------------------------------------------
async function createBooking(event) {
  event.preventDefault();

  const payload = {
    airline_code: document.getElementById("airline_code").value,
    passenger_name: document.getElementById("passenger_name").value.trim(),
    contact_number: document.getElementById("contact_number").value.trim(),
  };

  if (!payload.passenger_name || !payload.contact_number) {
    alert("Please fill in all fields.");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/bookings/create`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    const data = await res.json();

    if (res.ok) {
      const bookingData = {
        airline_code: payload.airline_code,
        passenger_name: payload.passenger_name,
        seat_number: data.seat_number,
        pnr: data.pnr,
        status: data.status,
      };
      localStorage.setItem("latest_booking", JSON.stringify(bookingData));
      window.location.href = "confirmation.html";
    } else {
      alert(data.detail || "Booking failed");
    }
  } catch (error) {
    console.error("Booking error:", error);
    alert("Error creating booking.");
  }
}

// -----------------------------------------------------
// 🔹 Confirmation Page Logic (confirmation.html)
// -----------------------------------------------------
if (window.location.pathname.includes("confirmation.html")) {
  const bookingData = JSON.parse(localStorage.getItem("latest_booking"));
  if (bookingData) {
    document.getElementById("passenger_name").textContent = bookingData.passenger_name;
    document.getElementById("airline_code").textContent = bookingData.airline_code;
    document.getElementById("seat_number").textContent = bookingData.seat_number;
    document.getElementById("pnr").textContent = bookingData.pnr;
  } else {
    document.getElementById("confirmation-details").innerHTML =
      "<p>No booking data found.</p>";
  }
}

function goToReceipt() {
  window.location.href = "receipt.html";
}

function goHome() {
  window.location.href = "index.html";
}

// -----------------------------------------------------
// 🔹 Receipt Page Logic (receipt.html)
// -----------------------------------------------------
if (window.location.pathname.includes("receipt.html")) {
  const bookingData = JSON.parse(localStorage.getItem("latest_booking"));
  const receiptDiv = document.getElementById("receipt-details");

  if (bookingData) {
    receiptDiv.innerHTML = `
      <p><b>PNR:</b> ${bookingData.pnr}</p>
      <p><b>Passenger:</b> ${bookingData.passenger_name}</p>
      <p><b>Airline Code:</b> ${bookingData.airline_code}</p>
      <p><b>Seat:</b> ${bookingData.seat_number}</p>
      <p><b>Status:</b> ${bookingData.status || "Confirmed"}</p>
    `;
  } else {
    receiptDiv.innerHTML = "<p>No booking receipt found.</p>";
  }
}

// -----------------------------------------------------
// 🔹 Download Receipt as PDF (receipt.html)
// -----------------------------------------------------
async function downloadPDF() {
  const bookingData = JSON.parse(localStorage.getItem("latest_booking"));
  if (!bookingData) {
    alert("No booking found!");
    return;
  }

  const pnr = bookingData.pnr;
  try {
    const res = await fetch(`${API_BASE}/bookings/${pnr}/receipt`);
    if (!res.ok) {
      alert("Failed to download receipt");
      return;
    }

    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `receipt_${pnr}.pdf`;
    a.click();
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error("Receipt download failed:", error);
    alert("Error downloading receipt");
  }
}
