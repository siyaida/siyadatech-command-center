export default function PaymentsPage() {
  return (
    <main className="min-h-screen bg-[#0a0a0f] text-[#f0f0f5] py-20 px-4">
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-10">
          <h1 className="text-4xl font-bold mb-4">Payments</h1>
          <p className="text-gray-400">Pay via mada, Visa, Mastercard, or Apple Pay.</p>
        </div>

        {/* Outstanding */}
        <div className="bg-[#13131f] border border-[#252536] rounded-xl p-8 mb-6">
          <h2 className="text-lg font-semibold mb-4">Outstanding Balance</h2>
          <div className="text-4xl font-bold text-[#a78bfa] mb-2">SAR 0.00</div>
          <p className="text-gray-400 text-sm">All payments are up to date.</p>
        </div>

        {/* Payment History */}
        <div className="bg-[#13131f] border border-[#252536] rounded-xl p-8 mb-6">
          <h2 className="text-lg font-semibold mb-4">Payment History</h2>
          <div className="space-y-3">
            {[
              { date: "May 1, 2026", desc: "Medical Spa Consultation", amount: "SAR 350", method: "mada" },
              { date: "Apr 15, 2026", desc: "Optometry Eye Exam", amount: "SAR 180", method: "Visa" },
              { date: "Mar 28, 2026", desc: "Dermatology Follow-up", amount: "SAR 220", method: "Apple Pay" },
            ].map((p, i) => (
              <div key={i} className="flex items-center justify-between bg-[#0a0a0f] rounded-lg p-4">
                <div>
                  <div className="font-medium">{p.desc}</div>
                  <div className="text-sm text-gray-400">{p.date} · {p.method}</div>
                </div>
                <div className="font-semibold">{p.amount}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Pay */}
        <div className="bg-[#13131f] border border-[#252536] rounded-xl p-8">
          <h2 className="text-lg font-semibold mb-4">Quick Pay</h2>
          <div className="grid grid-cols-2 gap-3">
            {["mada", "Visa", "Mastercard", "Apple Pay"].map((method) => (
              <button
                key={method}
                className="py-3 bg-[#0a0a0f] border border-[#252536] rounded-lg hover:border-[#8b5cf6] transition text-sm font-medium"
              >
                {method === "mada" ? "💳 mada" : `💳 ${method}`}
              </button>
            ))}
          </div>
          <p className="text-xs text-gray-500 mt-3">
            Powered by Geidea — SAMA licensed, KSA-native
          </p>
        </div>
      </div>
    </main>
  )
}
