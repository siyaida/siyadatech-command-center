export default function DashboardPage() {
  return (
    <main className="min-h-screen bg-[#0a0a0f] text-[#f0f0f5]">
      {/* Header */}
      <header className="border-b border-[#252536] px-6 py-4 flex items-center justify-between">
        <div className="font-bold text-xl">Ragaban <span className="text-[#8b5cf6]">Patient Portal</span></div>
        <div className="flex items-center gap-4">
          <span className="text-sm text-gray-400">Ahmed Al-Saud</span>
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-[#7c3aed] to-[#2563eb]" />
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <aside className="w-64 border-r border-[#252536] min-h-screen p-4 hidden md:block">
          <nav className="space-y-2">
            {[
              { label: "Overview", active: true },
              { label: "Appointments", active: false },
              { label: "Medical Records", active: false },
              { label: "Payments", active: false },
              { label: "Insurance", active: false },
              { label: "Messages", active: false },
            ].map((item) => (
              <a
                key={item.label}
                href="#"
                className={`block px-4 py-2 rounded-lg text-sm ${
                  item.active
                    ? "bg-[#8b5cf6]/10 text-[#a78bfa] border border-[#8b5cf6]/20"
                    : "text-gray-400 hover:bg-[#13131f] hover:text-white"
                }`}
              >
                {item.label}
              </a>
            ))}
          </nav>
        </aside>

        {/* Main Content */}
        <div className="flex-1 p-8">
          <h1 className="text-2xl font-bold mb-6">Overview</h1>

          {/* Stats Cards */}
          <div className="grid md:grid-cols-4 gap-4 mb-8">
            {[
              { label: "Upcoming Appointments", value: "2", color: "text-[#a78bfa]" },
              { label: "Total Visits", value: "12", color: "text-white" },
              { label: "Outstanding Balance", value: "SAR 0", color: "text-[#22c55e]" },
              { label: "Insurance Claims", value: "1 Pending", color: "text-[#f59e0b]" },
            ].map((stat) => (
              <div key={stat.label} className="bg-[#13131f] border border-[#252536] rounded-xl p-5">
                <div className={`text-3xl font-bold ${stat.color} mb-1`>{stat.value}</div>
                <div className="text-sm text-gray-400">{stat.label}</div>
              </div>
            ))}
          </div>

          {/* Upcoming Appointments */}
          <div className="bg-[#13131f] border border-[#252536] rounded-xl p-6 mb-8">
            <h2 className="text-lg font-semibold mb-4">Upcoming Appointments</h2>
            <div className="space-y-4">
              {[
                {
                  date: "May 15, 2026",
                  time: "10:00 AM",
                  dept: "Medical Spa",
                  branch: "Jeddah Main",
                  status: "Confirmed",
                  statusColor: "text-[#22c55e]",
                },
                {
                  date: "May 22, 2026",
                  time: "02:00 PM",
                  dept: "Optometry",
                  branch: "Jeddah North",
                  status: "Pending Payment",
                  statusColor: "text-[#f59e0b]",
                },
              ].map((apt, i) => (
                <div key={i} className="flex items-center justify-between bg-[#0a0a0f] rounded-lg p-4">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-[#7c3aed]/20 to-[#2563eb]/20 flex items-center justify-center text-lg">
                      {apt.dept === "Medical Spa" ? "💆" : "👁️"}
                    </div>
                    <div>
                      <div className="font-semibold">{apt.dept}</div>
                      <div className="text-sm text-gray-400">
                        {apt.date} at {apt.time} · {apt.branch}
                      </div>
                    </div>
                  </div>
                  <div className={`text-sm font-medium ${apt.statusColor}`>{apt.status}</div>
                </div>
              ))}
            </div>
            <a
              href="/book"
              className="inline-block mt-4 px-6 py-2 bg-gradient-to-r from-[#7c3aed] to-[#2563eb] rounded-lg text-sm font-semibold hover:opacity-90 transition"
            >
              + Book New Appointment
            </a>
          </div>

          {/* Recent Activity */}
          <div className="bg-[#13131f] border border-[#252536] rounded-xl p-6">
            <h2 className="text-lg font-semibold mb-4">Recent Activity</h2>
            <div className="space-y-3">
              {[
                { action: "Appointment completed", detail: "Medical Spa — Jeddah Main", time: "2 days ago", icon: "✅" },
                { action: "Insurance claim submitted", detail: "Claim #CLM-2026-001", time: "1 week ago", icon: "📋" },
                { action: "Payment received", detail: "SAR 350 via mada", time: "1 week ago", icon: "💳" },
              ].map((activity, i) => (
                <div key={i} className="flex items-center gap-3 text-sm">
                  <span>{activity.icon}</span>
                  <div className="flex-1">
                    <div>{activity.action}</div>
                    <div className="text-gray-400">{activity.detail}</div>
                  </div>
                  <div className="text-gray-500">{activity.time}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </main>
  )
}
