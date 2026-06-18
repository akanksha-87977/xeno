"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { vipAPI } from "@/lib/api";
import { Crown, MapPin, Mail, Phone, Calendar, RefreshCw } from "lucide-react";
import { formatDate } from "@/lib/utils";

export default function VIPCustomersPage() {
  const [vipCustomers, setVipCustomers] = useState<any[]>([]);
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    loadVIPData();
  }, []);

  const loadVIPData = async () => {
    try {
      const [customers, statsData] = await Promise.all([
        vipAPI.getAll(),
        vipAPI.getStats(),
      ]);
      setVipCustomers(customers);
      setStats(statsData);
    } catch (error) {
      console.error("Failed to load VIP data:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    setGenerating(true);
    try {
      await vipAPI.generate();
      await loadVIPData();
      alert("VIP customers generated successfully!");
    } catch (error) {
      alert("Failed to generate VIP customers");
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return <div className="text-center py-12">Loading VIP customers...</div>;
  }

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold mb-2 flex items-center gap-2">
            <Crown className="h-8 w-8 text-yellow-500" />
            VIP Customers
          </h1>
          <p className="text-muted-foreground">
            Premium customers from tier-1 cities with recent signups
          </p>
        </div>
        <Button onClick={handleGenerate} disabled={generating}>
          <RefreshCw className={`h-4 w-4 mr-2 ${generating ? "animate-spin" : ""}`} />
          {generating ? "Generating..." : "Generate VIP List"}
        </Button>
      </div>

      {/* Stats Overview */}
      {stats && (
        <div className="grid gap-6 md:grid-cols-3">
          <Card>
            <CardHeader>
              <CardTitle>Total VIP Customers</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-4xl font-bold text-yellow-600">
                {stats.total_vip_customers}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>VIP Criteria</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <div>
                <span className="text-sm text-muted-foreground">Cities:</span>
                <div className="font-medium">{stats.criteria.cities.join(", ")}</div>
              </div>
              <div>
                <span className="text-sm text-muted-foreground">Signup Window:</span>
                <div className="font-medium">Last {stats.criteria.days_threshold} days</div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>City Distribution</CardTitle>
            </CardHeader>
            <CardContent>
              {Object.entries(stats.city_distribution).map(([city, count]: [string, any]) => (
                <div key={city} className="flex justify-between py-1">
                  <span className="text-sm">{city}</span>
                  <span className="font-medium">{count}</span>
                </div>
              ))}
            </CardContent>
          </Card>
        </div>
      )}

      {/* VIP Customers List */}
      <Card>
        <CardHeader>
          <CardTitle>VIP Customer Directory</CardTitle>
          <CardDescription>
            {vipCustomers.length} premium customers eligible for VIP benefits
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4">
            {vipCustomers.map((customer) => (
              <div
                key={customer.customer_id}
                className="border rounded-lg p-4 hover:shadow-md transition-shadow bg-gradient-to-r from-yellow-50 to-white"
              >
                <div className="flex items-start justify-between">
                  <div className="space-y-2 flex-1">
                    <div className="flex items-center gap-2">
                      <Crown className="h-5 w-5 text-yellow-500" />
                      <h3 className="font-semibold text-lg">{customer.full_name}</h3>
                      <span className="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">
                        VIP
                      </span>
                    </div>
                    
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div className="flex items-center gap-2">
                        <Mail className="h-4 w-4 text-muted-foreground" />
                        <span>{customer.email}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Phone className="h-4 w-4 text-muted-foreground" />
                        <span>{customer.phone_number}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <MapPin className="h-4 w-4 text-muted-foreground" />
                        <span>{customer.city}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Calendar className="h-4 w-4 text-muted-foreground" />
                        <span>{formatDate(customer.signup_date)}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {vipCustomers.length === 0 && (
            <div className="text-center py-12 text-muted-foreground">
              No VIP customers found. Click "Generate VIP List" to create the list.
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}