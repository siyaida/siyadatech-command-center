export default function HomePage() {
  return (
    <main className="min-h-screen bg-[#0a0a0f] text-[#f0f0f5]">
      {/* Hero */}
      <section className="flex flex-col items-center justify-center py-24 px-4 text-center">
        <div className="inline-flex items-center gap-2 bg-[#13131f] border border-[#252536] rounded-full px-4 py-2 mb-8 text-sm text-[#a78bfa]">
          <span className="w-2 h-2 rounded-full bg-[#8b5cf6] animate-pulse" />
          <span className="font-mono">RAGABAN CLINICS — JEDDAH</span>
        </div>
        <h1 className="text-5xl md:text-7xl font-bold tracking-tight mb-6">
          Your Health, <span className="text-[#8b5cf6]">Digital</span>
        </h1>
        <p className="text-xl text-gray-400 max-w-2xl mb-10">
          Book appointments, view medical records, make payments — all in one place.
          Four locations across Jeddah. Premium care, now digital.
        </p>
        <div className="flex gap-4">
          <a
            href="#book"
            className="px-8 py-3 bg-gradient-to-r from-[#7c3aed] to-[#2563eb] rounded-lg font-semibold hover:opacity-90 transition"
          >
            Book Appointment
          </a>
          <a
            href="#services"
            className="px-8 py-3 bg-[#13131f] border border-[#252536] rounded-lg font-semibold hover:border-[#35354f] transition"
          >
            Our Services
          </a>
        </div>
      </section>

      {/* Services */}
      <section id="services" className="py-20 px-4 max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold text-center mb-12">Our Services</h2>
        <div className="grid md:grid-cols-3 gap-6">
          {[
            { icon: "💆", title: "Medical Spa", desc: "Advanced aesthetic treatments, laser therapy, and cosmetic dermatology." },
            { icon: "👁️", title: "Optometry", desc: "Comprehensive eye exams, contact lenses, and optical services." },
            { icon: "🏥", title: "General Medicine", desc: "Primary care, diagnostics, and specialist referrals." },
          ].map((s) => (
            <div key={s.title} className="bg-[#13131f] border border-[#252536] rounded-xl p-6 hover:border-[#35354f] transition">
              <div className="text-3xl mb-4">{s.icon}</div>
              <h3 className="text-xl font-semibold mb-2">{s.title}</h3>
              <p className="text-gray-400">{s.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Branches */}
      <section className="py-20 px-4 max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold text-center mb-12">Our Locations</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            { name: "Jeddah Main", address: "Al-Rawdah District, Main St.", phone: "+966 12 345 6789" },
            { name: "Jeddah North", address: "Al-Hamra District, Prince Sultan St.", phone: "+966 12 345 6790" },
            { name: "Branch 3", address: "Al-Mohammadiyah District", phone: "+966 12 345 6791" },
            { name: "Branch 4", address: "Al-Salamah District", phone: "+966 12 345 6792" },
          ].map((b) => (
            <div key={b.name} className="bg-[#13131f] border border-[#252536] rounded-xl p-5">
              <h3 className="font-semibold text-[#a78bfa] mb-2">{b.name}</h3>
              <p className="text-sm text-gray-400 mb-1">{b.address}</p>
              <p className="text-sm font-mono">{b.phone}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-[#252536] py-10 text-center text-gray-500 text-sm">
        <p> Ragaban Clinics. All rights reserved.</p>
        <p className="mt-2">Powered by Siyadatech — KSA Healthcare AI Transformation</p>
      </footer>
    </main>
  )
}
