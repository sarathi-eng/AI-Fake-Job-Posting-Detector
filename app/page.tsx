import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import Features from "../components/Features";
import ApiAvailability from "../components/ApiAvailability";
import Footer from "../components/Footer";

export default function HomePage() {
  return (
    <main className="min-h-dvh">
      <Navbar />

      <section id="home" className="relative overflow-hidden">
        <div className="pointer-events-none absolute inset-0">
          <div className="absolute -top-24 left-1/2 h-[520px] w-[820px] -translate-x-1/2 rounded-full bg-indigo-500/20 blur-3xl" />
          <div className="absolute -bottom-40 right-[-120px] h-[520px] w-[520px] rounded-full bg-fuchsia-500/15 blur-3xl" />
        </div>

        <div className="mx-auto w-full max-w-6xl px-6 pt-28 pb-14">
          <Hero />
        </div>
      </section>

      <section id="features" className="mx-auto w-full max-w-6xl px-6 py-14">
        <Features />
      </section>

      <section id="demo" className="mx-auto w-full max-w-6xl px-6 py-14">
        <ApiAvailability />
      </section>

      <Footer />
    </main>
  );
}
