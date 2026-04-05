"use client";

import { useState, useEffect } from "react";
import { 
  Tent, MessageSquare, 
  PlusCircle, CreditCard,
  ChevronRight, Clock, Package,
  ShieldCheck, Zap, Camera,
  CheckCircle, Globe
} from "lucide-react";
import styles from "./page.module.css";

export default function HostDashboard() {
  const [activeTab, setActiveTab] = useState("listings");
  const [isVerified] = useState(false);
  const [onboardingStep, setOnboardingStep] = useState(1);
  const [loading, setLoading] = useState(false);

  // Mock verification check
  useEffect(() => {
    const checkStatus = async () => {
      // In prod, call /api/user/profile to check kyc_status
    };
    checkStatus();
  }, []);

  const handleStartOnboarding = () => {
    setOnboardingStep(2);
  };

  const handleCompleteKYC = () => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setOnboardingStep(3);
    }, 1500);
  };

  if (!isVerified && onboardingStep < 4) {
    return (
      <div className={styles.onboardingContainer}>
        <div className={styles.onboardingCard}>
          {onboardingStep === 1 && (
            <div className={styles.onboardingContent}>
              <div className={styles.onboardingIcon}><ShieldCheck size={48} color="#10b981" /></div>
              <h2 className={styles.onboardingTitle}>Become a Verified Host</h2>
              <p className={styles.onboardingSub}>To list your services on ISEYAA, Ogun State Government requires a verified Host profile.</p>
              <div className={styles.benefits}>
                <div className={styles.benefit}><Zap size={16} /> <span>Get the &quot;Verified&quot; badge</span></div>
                <div className={styles.benefit}><Globe size={16} /> <span>Global visibility for your service</span></div>
                <div className={styles.benefit}><CheckCircle size={16} /> <span>Secure automated payouts</span></div>
              </div>
              <button className={styles.primBtn} onClick={handleStartOnboarding}>Start Application <ChevronRight size={18} /></button>
            </div>
          )}

          {onboardingStep === 2 && (
            <div className={styles.onboardingContent}>
              <h2 className={styles.onboardingTitle}>Identity Verification</h2>
              <p className={styles.onboardingSub}>Upload your NIN or International Passport for Squad Alpha review.</p>
              <div className={styles.uploadBox}>
                <Camera size={32} color="#64748b" />
                <p>Click to upload document photo</p>
                <input type="file" className={styles.fileInput} />
              </div>
              <button className={styles.primBtn} onClick={handleCompleteKYC} disabled={loading}>
                {loading ? "Processing..." : "Submit Identity"}
              </button>
            </div>
          )}

          {onboardingStep === 3 && (
            <div className={styles.onboardingContent}>
              <div className={styles.onboardingIcon}><Clock size={48} color="#f59e0b" /></div>
              <h2 className={styles.onboardingTitle}>Pending Review</h2>
              <p className={styles.onboardingSub}>Your application is being reviewed by the Ogun State Tourism Board. This usually takes 24 hours.</p>
              <button className={styles.secBtn} onClick={() => setOnboardingStep(4)}>Preview Dashboard (Read Only)</button>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className={styles.container}>
      {/* Sidebar */}
      <aside className={styles.sidebar}>
        <div className={styles.brand}>
          <div className={styles.logo}>🌿</div>
          <div>
            <h1 className={styles.brandName}>ISEYAA</h1>
            <p className={styles.brandTag}>Host Dashboard</p>
          </div>
        </div>

        <nav className={styles.nav}>
          <div className={styles.navSection}>Business</div>
          <button className={`${styles.navItem} ${activeTab === "listings" ? styles.active : ""}`} onClick={() => setActiveTab("listings")}>
            <Tent size={18} /> My Listings
          </button>
          <button className={`${styles.navItem} ${activeTab === "orders" ? styles.active : ""}`} onClick={() => setActiveTab("orders")}>
            <Package size={18} /> Orders & Bookings
          </button>
          <button className={`${styles.navItem}`}>
            <MessageSquare size={18} /> Messages
          </button>
          
          <div className={styles.navSection}>Finance</div>
          <button className={`${styles.navItem}`}>
            <CreditCard size={18} /> Wallet & Payouts
          </button>
        </nav>

        <div className={styles.sidebarFooter}>
          <div className={styles.profile}>
            <div className={styles.avatar}>LS</div>
            <div>
              <p className={styles.userName}>Local Star</p>
              <p className={styles.userRole}>Artisan & Guide</p>
            </div>
          </div>
          
          {/* Switcher */}
          <div className={styles.switcherBlock}>
            <p className={styles.switcherLabel}>Profile Mode</p>
            <div className={styles.switcher}>
              <button className={styles.switchBtn} onClick={() => window.location.href='http://localhost:3000'}>Traveler</button>
              <button className={`${styles.switchBtn} ${styles.switchBtnActive}`}>Host</button>
              <button className={styles.switchBtn} onClick={() => window.location.href='http://localhost:3001'}>Govt</button>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className={styles.main}>
        <header className={styles.header}>
          <div>
            <h2 className={styles.pageTitle}>Welcome back, Host</h2>
            <p className={styles.pageSub}>Manage your services and connect with travelers in Ogun State.</p>
          </div>
          <button className={styles.addBtn}><PlusCircle size={20} /> Create New Listing</button>
        </header>

        <section className={styles.grid}>
          <div className={styles.card}>
            <div className={styles.cardHeader}>
              <h3 className={styles.cardTitle}>Current Listings</h3>
              <span className={styles.cardBadge}>3 Active</span>
            </div>
            <div className={styles.listingList}>
              <div className={styles.listingItem}>
                <div className={styles.listingImg} style={{ background: "#1e293b" }}>🌿</div>
                <div className={styles.listingInfo}>
                  <p className={styles.listingName}>Olumo Rock Secret Trail</p>
                  <p className={styles.listingMeta}>₦12,500 · Heritage Guide</p>
                </div>
                <ChevronRight size={16} color="#475569" />
              </div>
              <div className={styles.listingItem}>
                <div className={styles.listingImg} style={{ background: "#064e3b" }}>🏨</div>
                <div className={styles.listingInfo}>
                  <p className={styles.listingName}>Forest Edge Eco-Lodge</p>
                  <p className={styles.listingMeta}>₦45,000 · Stay</p>
                </div>
                <ChevronRight size={16} color="#475569" />
              </div>
            </div>
          </div>

          <div className={styles.card}>
            <div className={styles.cardHeader}>
              <h3 className={styles.cardTitle}>Earnings</h3>
              <span className={styles.cardBadge}>This Month</span>
            </div>
            <div className={styles.earnings}>
              <div className={styles.earningsVal}>₦240,500</div>
              <p className={styles.earningsSub}>+12% from last month</p>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
