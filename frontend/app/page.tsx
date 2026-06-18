import Link from "next/link";
import { Button } from "../components/ui/button";
import { CheckCircle, BarChart3, Shield, Zap } from "lucide-react";


export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-blue-50 to-white">
      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20">
        <div className="text-center max-w-4xl mx-auto">
          <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-6">
            Global Transaction Validator &
            <span className="text-primary"> Customer Intelligence</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Enterprise-grade platform for transaction validation, customer data
            management, analytics, and intelligent reporting.
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/register">
              <Button size="lg" className="text-lg px-8">
                Get Started Free
              </Button>
            </Link>
            <Link href="/login">
              <Button size="lg" variant="outline" className="text-lg px-8">
                Sign In
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="container mx-auto px-4 py-20">
        <h2 className="text-3xl font-bold text-center mb-12">
          Powerful Features
        </h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          <FeatureCard
            icon={<CheckCircle className="h-10 w-10 text-green-500" />}
            title="Smart Validation"
            description="AI-powered data validation with country-specific rules for phone, email, and date formats."
          />
          <FeatureCard
            icon={<BarChart3 className="h-10 w-10 text-blue-500" />}
            title="Advanced Analytics"
            description="Real-time dashboards with customer insights, transaction trends, and SQL analytics."
          />
          <FeatureCard
            icon={<Shield className="h-10 w-10 text-purple-500" />}
            title="Enterprise Security"
            description="JWT authentication, role-based access control, and comprehensive audit logs."
          />
          <FeatureCard
            icon={<Zap className="h-10 w-10 text-yellow-500" />}
            title="Automated Processing"
            description="Auto data cleaning, enrichment, VIP customer generation, and file splitting."
          />
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-primary text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold mb-4">
            Ready to transform your data management?
          </h2>
          <p className="text-xl mb-8 opacity-90">
            Join thousands of companies using our platform
          </p>
          <Link href="/register">
            <Button size="lg" variant="secondary" className="text-lg px-8">
              Start Your Free Trial
            </Button>
          </Link>
        </div>
      </section>
    </div>
  );
}

function FeatureCard({ icon, title, description }: any) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
      <div className="mb-4">{icon}</div>
      <h3 className="text-xl font-semibold mb-2">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}