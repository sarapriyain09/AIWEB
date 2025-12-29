import { Link } from "react-router-dom";

export default function LandingPage() {
  return (
    <div className="bg-white font-sans text-gray-800">
      {/* Top Navbar */}
      <header className="sticky top-0 z-50 border-b bg-white/90 backdrop-blur">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between gap-4">
            <Link to="/" className="flex items-center">
              <img src="/img/clai-logo.svg" alt="CLAi" className="h-8 w-auto" />
            </Link>

            <nav className="hidden items-center gap-6 md:flex">
              <a className="text-sm text-gray-700 hover:text-gray-900" href="#features">
                Features
              </a>
              <a className="text-sm text-gray-700 hover:text-gray-900" href="#how-it-works">
                How it works
              </a>
              <a className="text-sm text-gray-700 hover:text-gray-900" href="#pricing">
                Pricing
              </a>
            </nav>

            <div className="flex items-center gap-2">
              <Link
                to="/login"
                className="rounded-lg px-4 py-2 text-sm font-semibold text-gray-700 hover:bg-gray-100"
              >
                Sign in
              </Link>
              <Link
                to="/register"
                className="rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500"
              >
                Get started
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="bg-gradient-to-r from-indigo-500 to-blue-400 text-white py-24">
        <div className="container mx-auto px-6 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            Build Real Web Apps with AI – No Experience Needed
          </h1>
          <p className="text-lg md:text-xl mb-6">
            From idea to deployable SaaS – AI generates full-stack code with payments in minutes.
          </p>

          <div className="flex justify-center gap-4">
            <Link
              to="/register"
              className="bg-yellow-400 text-gray-900 font-semibold px-6 py-3 rounded-lg hover:bg-yellow-300 transition"
            >
              Get Started Free
            </Link>
            <a
              href="#how-it-works"
              className="bg-white text-indigo-600 font-semibold px-6 py-3 rounded-lg hover:bg-gray-100 transition"
            >
              Watch Demo
            </a>
          </div>

          <div className="mt-10">
            <div className="mx-auto max-w-6xl">
              <div className="grid grid-cols-1 gap-4 md:grid-cols-12">
                <div className="md:col-span-7 rounded-lg bg-white/10 shadow-lg backdrop-blur md:h-[28rem] overflow-hidden">
                  <img
                    src="/img/head-image.png"
                    alt="AI web app builder hero preview"
                    className="h-full w-full object-cover"
                  />
                </div>

                <div className="md:col-span-5 grid grid-cols-2 grid-rows-2 gap-4 md:h-[28rem]">
                  <div className="rounded-lg bg-white/10 shadow-lg backdrop-blur overflow-hidden">
                    <img
                      src="/img/describe-your-app.png"
                      alt="Describe your app"
                      className="h-full w-full object-cover"
                    />
                  </div>
                  <div className="rounded-lg bg-white/10 shadow-lg backdrop-blur overflow-hidden">
                    <img
                      src="/img/ai-generate-code.png"
                      alt="AI generates your code"
                      className="h-full w-full object-cover"
                    />
                  </div>
                  <div className="rounded-lg bg-white/10 shadow-lg backdrop-blur overflow-hidden">
                    <img
                      src="/img/full-stack.png"
                      alt="Full stack"
                      className="h-full w-full object-cover"
                    />
                  </div>
                  <div className="rounded-lg bg-white/10 shadow-lg backdrop-blur overflow-hidden">
                    <img
                      src="/img/stripe-payment.png"
                      alt="Stripe payments"
                      className="h-full w-full object-cover"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-gray-50">
        <div className="container mx-auto px-6 text-center">
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <img
                src="/img/full-stack.png"
                alt="Full-stack app generation"
                className="mx-auto mb-4 h-16 w-auto rounded"
              />
              <h3 className="text-xl font-bold mb-2">Full-Stack App Generation</h3>
              <p>Frontend, backend &amp; database generated automatically.</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <img
                src="/img/stripe-payment.png"
                alt="Stripe payments"
                className="mx-auto mb-4 h-16 w-auto rounded"
              />
              <h3 className="text-xl font-bold mb-2">Stripe Payments Built-In</h3>
              <p>Subscriptions and payments ready to go.</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <img
                src="/img/learn-edit-code.png"
                alt="Learn and edit code"
                className="mx-auto mb-4 h-16 w-auto rounded"
              />
              <h3 className="text-xl font-bold mb-2">Learn &amp; Edit Code</h3>
              <p>Customizable, deployment-ready code with learning guidance.</p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section id="how-it-works" className="py-20">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold mb-8">How It Works</h2>
          <p className="mb-12">Create your app in 3 easy steps.</p>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-4">1</div>
              <img
                src="/img/describe-your-app.png"
                alt="Describe your app"
                className="mx-auto mb-4 h-24 w-auto rounded"
              />
              <h3 className="text-xl font-bold mb-2">Describe Your App</h3>
              <p>Tell us your idea in plain language.</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-4">2</div>
              <img
                src="/img/ai-generate-code.png"
                alt="AI generates your code"
                className="mx-auto mb-4 h-24 w-auto rounded"
              />
              <h3 className="text-xl font-bold mb-2">AI Generates Your Code</h3>
              <p>Full-stack app created instantly.</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <div className="text-4xl mb-4">3</div>
              <img
                src="/img/launch-monetize-dashboard.svg"
                alt="Launch and monetize"
                className="mx-auto mb-4 h-24 w-auto max-w-full"
              />
              <h3 className="text-xl font-bold mb-2">Launch &amp; Monetize</h3>
              <p>Deploy live and start earning.</p>
            </div>
          </div>

          <div className="mt-10">
            <Link
              to="/login"
              className="inline-block text-sm text-indigo-700 font-semibold hover:underline"
            >
              Already have an account? Sign in
            </Link>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="pricing" className="py-20 bg-gray-50">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold mb-12">Student-Friendly Plans</h2>
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <div className="bg-white p-8 rounded-lg shadow hover:shadow-lg transition">
              <h3 className="text-xl font-bold mb-4">Student Plan</h3>
              <p className="text-2xl font-bold mb-4">$10 / month</p>
              <p className="mb-4">200 AI credits</p>
              <ul className="mb-6 text-left list-disc list-inside space-y-1">
                <li>Full-stack apps</li>
                <li>Stripe integration</li>
                <li>Editable code</li>
              </ul>
              <Link
                to="/register"
                className="inline-block bg-indigo-600 text-white font-semibold px-6 py-3 rounded-lg hover:bg-indigo-500 transition"
              >
                Get Started
              </Link>
            </div>

            <div className="bg-white p-8 rounded-lg shadow hover:shadow-lg transition">
              <h3 className="text-xl font-bold mb-4">Pro Plan</h3>
              <p className="text-2xl font-bold mb-4">$25 / month</p>
              <p className="mb-4">1000 AI credits</p>
              <ul className="mb-6 text-left list-disc list-inside space-y-1">
                <li>Advanced features</li>
                <li>Priority support</li>
                <li>More credits</li>
              </ul>
              <Link
                to="/register"
                className="inline-block bg-yellow-400 text-gray-900 font-semibold px-6 py-3 rounded-lg hover:bg-yellow-300 transition"
              >
                Upgrade Now
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20">
        <div className="container mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold mb-12">What Users Say</h2>
          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <p className="italic mb-4">
                “I built my first SaaS app in under an hour!”
              </p>
              <p className="font-bold">— Sarah, Student Developer</p>
            </div>
            <div className="bg-white p-6 rounded-lg shadow hover:shadow-lg transition">
              <p className="italic mb-4">
                “Perfect for launching my projects fast!”
              </p>
              <p className="font-bold">— Mark, Indie Developer</p>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-indigo-600 text-white py-8">
        <div className="container mx-auto px-6 text-center space-y-2">
          <p>© {new Date().getFullYear()} Learn2Build – Build Your Dreams</p>
          <div className="flex justify-center space-x-4">
            <a href="#" className="hover:underline">
              About
            </a>
            <a href="#" className="hover:underline">
              Blog
            </a>
            <a href="#" className="hover:underline">
              Docs
            </a>
            <a href="#" className="hover:underline">
              Contact
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
}
