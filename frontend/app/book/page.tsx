export default function BookingPage() {
  return (
    <main className="min-h-screen bg-[#0a0a0f] text-[#f0f0f5] py-20 px-4">
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-10">
          <h1 className="text-4xl font-bold mb-4">Book Appointment</h1>
          <p className="text-gray-400">Select your branch, department, and preferred time.</p>
        </div>

        <form className="bg-[#13131f] border border-[#252536] rounded-xl p-8 space-y-6">
          {/* Branch */}
          <div>
            <label className="block text-sm font-medium mb-2">Branch</label>
            <select className="w-full bg-[#0a0a0f] border border-[#252536] rounded-lg px-4 py-3 focus:border-[#8b5cf6] outline-none">
              <option>Jeddah Main — Al-Rawdah</option>
              <option>Jeddah North — Al-Hamra</option>
              <option>Branch 3 — Al-Mohammadiyah</option>
              <option>Branch 4 — Al-Salamah</option>
            </select>
          </div>

          {/* Department */}
          <div>
            <label className="block text-sm font-medium mb-2">Department</label>
            <select className="w-full bg-[#0a0a0f] border border-[#252536] rounded-lg px-4 py-3 focus:border-[#8b5cf6] outline-none">
              <option>Medical Spa</option>
              <option>Optometry</option>
              <option>Dermatology</option>
              <option>General Medicine</option>
            </select>
          </div>

          {/* Date */}
          <div>
            <label className="block text-sm font-medium mb-2">Preferred Date</label>
            <input
              type="date"
              className="w-full bg-[#0a0a0f] border border-[#252536] rounded-lg px-4 py-3 focus:border-[#8b5cf6] outline-none"
            />
          </div>

          {/* Time */}
          <div>
            <label className="block text-sm font-medium mb-2">Preferred Time</label>
            <select className="w-full bg-[#0a0a0f] border border-[#252536] rounded-lg px-4 py-3 focus:border-[#8b5cf6] outline-none">
              <option>09:00 AM</option>
              <option>10:00 AM</option>
              <option>11:00 AM</option>
              <option>12:00 PM</option>
              <option>01:00 PM</option>
              <option>02:00 PM</option>
              <option>03:00 PM</option>
              <option>04:00 PM</option>
              <option>05:00 PM</option>
              <option>06:00 PM</option>
              <option>07:00 PM</option>
              <option>08:00 PM</option>
            </select>
          </div>

          {/* National ID */}
          <div>
            <label className="block text-sm font-medium mb-2">National ID</label>
            <input
              type="text"
              placeholder="10 digits"
              maxLength={10}
              className="w-full bg-[#0a0a0f] border border-[#252536] rounded-lg px-4 py-3 focus:border-[#8b5cf6] outline-none"
            />
          </div>

          {/* Phone */}
          <div>
            <label className="block text-sm font-medium mb-2">Phone</label>
            <input
              type="tel"
              placeholder="+966 5XX XXX XXX"
              className="w-full bg-[#0a0a0f] border border-[#252536] rounded-lg px-4 py-3 focus:border-[#8b5cf6] outline-none"
            />
          </div>

          {/* Notes */}
          <div>
            <label className="block text-sm font-medium mb-2">Reason for Visit</label>
            <textarea
              rows={3}
              placeholder="Brief description of your visit..."
              className="w-full bg-[#0a0a0f] border border-[#252536] rounded-lg px-4 py-3 focus:border-[#8b5cf6] outline-none"
            />
          </div>

          {/* Submit */}
          <button
            type="submit"
            className="w-full py-4 bg-gradient-to-r from-[#7c3aed] to-[#2563eb] rounded-lg font-semibold hover:opacity-90 transition"
          >
            Confirm Booking
          </button>

          <p className="text-xs text-gray-500 text-center">
            You will receive a WhatsApp confirmation within 2 minutes.
          </p>
        </form>
      </div>
    </main>
  )
}
