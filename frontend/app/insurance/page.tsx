export default function InsurancePage() {
  return (
    <main className="min-h-screen bg-[#0a0a0f] text-[#f0f0f5] py-20 px-4">
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-10">
          <h1 className="text-4xl font-bold mb-4">Insurance</h1>
          <p className="text-gray-400">Check eligibility and track claims via NPHIES.</p>
        </div>

        {/* Eligibility Check */}
        <div className="bg-[#13131f] border border-[#252536] rounded-xl p-8 mb-6">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <span>🔍</span> Check Eligibility
          </h2>
          <div className="flex gap-3">
            <input
              type="text"
              placeholder="Enter National ID"
              maxLength={10}
              className="flex-1 bg-[#0a0a0f] border border-[#252536] rounded-lg px-4 py-3 focus:border-[#8b5cf6] outline-none"
            />
            <button className="px-6 py-3 bg-gradient-to-r from-[#7c3aed] to-[#2563eb] rounded-lg font-semibold hover:opacity-90 transition">
              Check
            </button>
          </div>
          <p className="text-xs text-gray-500 mt-2">
            Powered by NPHIES FHIR — CHI.gov.sa
          </p>
        </div>

        {/* Claims List */}
        <div className="bg-[#13131f] border border-[#252536] rounded-xl p-8">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <span>📋</span> Your Claims
          </h2>
          <div className="space-y-3">
            {[
              { id: "CLM-2026-001", date: "May 1, 2026", amount: "SAR 450", status: "Approved", statusColor: "text-[#22c55e]" },
              { id: "CLM-2026-002", date: "May 8, 2026", amount: "SAR 320", status: "Pending", statusColor: "text-[#f59e0b]" },
            ].map((claim) => (
              <div key={claim.id} className="flex items-center justify-between bg-[#0a0a0f] rounded-lg p-4">
                <div>
                  <div className="font-medium">{claim.id}</div>
                  <div className="text-sm text-gray-400">{claim.date} · {claim.amount}</div>
                </div>
                <div className={`text-sm font-semibold ${claim.statusColor}`}>{claim.status}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </main>
  )
}
