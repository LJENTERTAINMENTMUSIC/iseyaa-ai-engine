"use client";

import { useState, useEffect } from "react";
import { 
  BarChart3, LayoutDashboard, Map,
  User, Activity, Users, Globe, ShieldCheck,
  ChevronRight, ArrowUpRight, Search
} from "lucide-react";
import styles from "./page.module.css";

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState("overview");
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    // Phase 3: Fetch telemetry from Intelligence Engine
    const fetchStats = async () => {
      try {
        const res = await fetch("http://localhost:8000/api/admin/stats", {
          headers: { "Authorization": "govt-token-verified" }
        });
        if (res.ok) {
          const data = await res.json();
          setStats(data);
        }
      } catch (err) {
        console.error("Dashboard engine link failed:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchStats();
  }, []);

  const kycQueue = [
    { id: "KYC-9281-2024", type: "NIN", region: "Ijebu-Ode", status: "processing", urgency: "high" },
    { id: "KYC-4412-2024", type: "Passport", region: "Abeokuta South", status: "verified", urgency: "normal" },
    { id: "KYC-1022-2024", type: "Voter ID", region: "Sagamu", status: "processing", urgency: "normal" },
    { id: "KYC-3389-2024", type: "NIN", region: "Ikenne", status: "rejected", urgency: "high" },
  ];

  return (
    <div className={styles.container}>
      {/* Sidebar - Node Navigation */}
      <aside className={styles.sidebar}>
        <div className={styles.brand}>
          <div className={styles.logo}>🌿</div>
          <div>
            <h1 className={styles.brandName}>ISEYAA IX</h1>
            <p className={styles.brandTag}>State intelligence node</p>
          </div>
        </div>

        <nav className={styles.nav}>
          <div className={styles.navSection}>Economic Engine</div>
          <button className={`${styles.navItem} ${activeTab === "overview" ? styles.active : ""}`} onClick={() => setActiveTab("overview")}>
            <LayoutDashboard size={18} /> OS Overview
          </button>
          <button className={`${styles.navItem} ${activeTab === "revenue" ? styles.active : ""}`} onClick={() => setActiveTab("revenue")}>
            <BarChart3 size={18} /> LGA Revenue
          </button>
          
          <div className={styles.navSection}>Human Assets</div>
          <button className={`${styles.navItem} ${activeTab === "kyc" ? styles.active : ""}`} onClick={() => setActiveTab("kyc")}>
            <ShieldCheck size={18} /> Trust/KYC Queue
          </button>
          <button className={`${styles.navItem} ${activeTab === "lgas" ? styles.active : ""}`} onClick={() => setActiveTab("lgas")}>
            <Map size={18} /> Regional Profiles
          </button>
        </nav>

        <div className={styles.sidebarFooter}>
          <div className={styles.profile}>
            <div className={styles.avatar}>GO</div>
            <div>
              <p className={styles.userName}>Gov Official</p>
              <p className={styles.userRole}>Node: Abeokuta South</p>
            </div>
          </div>
          
          <div className={styles.switcherBlock}>
            <p className={styles.switcherLabel}>TiarionX Ecosystem</p>
            <div className={styles.switcher}>
              <button className={styles.switchBtn} onClick={() => window.location.href='http://localhost:3000'}>ISEYAA Travel</button>
              <button className={`${styles.switchBtn} ${styles.switchBtnActive}`}>Gov Command</button>
            </div>
          </div>
        </div>
      </aside>

      {/* Primary Intelligence Feed */}
      <main className={styles.main}>
        <header className={styles.header}>
          <div>
            <h2 className={styles.pageTitle}>
              {activeTab === "overview" && "Ogun State Diagnostics"}
              {activeTab === "kyc" && "Identity Protocol Verification"}
              {activeTab === "lgas" && "Regional IQ Node Mapping"}
            </h2>
            <p className={styles.pageSub}>
              {activeTab === "overview" && "Telemetry from all 20 LGA economic nodes."}
              {activeTab === "kyc" && "Reviewing Phase 3 verified identity submissions."}
              {activeTab === "lgas" && "Cultural and historical data synchronization."}
            </p>
          </div>
          <div className={styles.headerActions}>
            <div className={searchQuery ? styles.searchActive : styles.searchBox}>
              <Search size={18} color="#64748b" />
              <input type="text" placeholder="Search LGA Node..." onChange={(e) => setSearchQuery(e.target.value)} />
            </div>
            <div className={styles.uptime}>● Engine v1.1 Active</div>
          </div>
        </header>

        {activeTab === "overview" && (
          <>
            <section className={styles.grid}>
              <div className={styles.statCard}>
                <div className={styles.statGlow} />
                <Activity className={styles.statIcon} color="#10b981" />
                <div className={styles.statHeader}>
                  <div className={styles.statValue}>{loading ? "..." : (stats?.visitor_growth || "+12.5%")}</div>
                  <ArrowUpRight size={16} color="#10b981" />
                </div>
                <div className={styles.statLabel}>State Participation</div>
              </div>
              <div className={styles.statCard}>
                <div className={styles.statGlow} />
                <Users className={styles.statIcon} color="#6366f1" />
                <div className={styles.statValue}>{loading ? "..." : (stats?.active_hosts || "1,420")}</div>
                <div className={styles.statLabel}>Verified Citizens</div>
              </div>
              <div className={styles.statCard}>
                <div className={styles.statGlow} />
                <Activity className={styles.statIcon} color="#f59e0b" />
                <div className={styles.statValue}>₦52.8M</div>
                <div className={styles.statLabel}>Tourism Revenue (OHA)</div>
              </div>
              <div className={styles.statCard}>
                <div className={styles.statGlow} />
                <Globe className={styles.statIcon} color="#3b82f6" />
                <div className={styles.statValue}>{loading ? "..." : (stats?.revenue_total || "₦450.2M")}</div>
                <div className={styles.statLabel}>Economic Velocity</div>
              </div>
            </section>

            {/* OHA Discovery Section */}
            <section className={styles.kycSection} style={{ marginBottom: '20px', padding: '20px', background: 'rgba(255,255,255,0.02)', borderRadius: '12px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
                  <h3 style={{ fontSize: '18px', fontWeight: '600' }}>Discovered Businesses (Crawler Node)</h3>
                  <button className={styles.uptime}>Trigger Regional Scan</button>
                </div>
                <div className={styles.kycTable}>
                  <div className={styles.tableHeader}>
                    <span>Business Name</span>
                    <span>Source</span>
                    <span>Region</span>
                    <span>Status</span>
                    <span>Action</span>
                  </div>
                  <div className={styles.tableRow}>
                    <span className={styles.cellId}>Lafia Hotel & Suites</span>
                    <span className={styles.cellType}><span className={styles.statusPill} style={{ background: '#3b82f6' }}>Google Maps</span></span>
                    <span className={styles.cellRegion}>Abeokuta South</span>
                    <span className={`${styles.cellStatus} ${styles.processing}`}>Discovered</span>
                    <div className={styles.cellActions}>
                      <button className={styles.actionView}>Send Invite</button>
                    </div>
                  </div>
                  <div className={styles.tableRow}>
                    <span className={styles.cellId}>Royal Shortlet A3</span>
                    <span className={styles.cellType}><span className={styles.statusPill} style={{ background: '#8b5cf6' }}>Instagram</span></span>
                    <span className={styles.cellRegion}>Ijebu Ode</span>
                    <span className={`${styles.cellStatus} ${styles.processing}`}>Discovered</span>
                    <div className={styles.cellActions}>
                      <button className={styles.actionView}>Send Invite</button>
                    </div>
                  </div>
                </div>
            </section>

            {/* OEMG Event Discovery Section (Phase 5) */}
            <section className={styles.kycSection} style={{ marginBottom: '20px', padding: '20px', background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(245, 158, 11, 0.2)', borderRadius: '12px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
                  <h3 style={{ fontSize: '18px', fontWeight: '600', color: '#f59e0b' }}>Event Intelligence (Cultural Node)</h3>
                  <button className={styles.uptime} style={{ borderColor: '#f59e0b', color: '#f59e0b' }}>Scan Social Signals</button>
                </div>
                <div className={styles.kycTable}>
                  <div className={styles.tableHeader}>
                    <span>Event Title</span>
                    <span>Category</span>
                    <span>LGA Node</span>
                    <span>Date</span>
                    <span>Action</span>
                  </div>
                  <div className={styles.tableRow}>
                    <span className={styles.cellId}>Ojude Oba Pre-Gala</span>
                    <span className={styles.cellType}><span className={styles.statusPill} style={{ background: '#f59e0b' }}>Festival</span></span>
                    <span className={styles.cellRegion}>Ijebu Ode</span>
                    <span className={styles.cellType}>Aug 12, 2024</span>
                    <div className={styles.cellActions}>
                      <button className={styles.actionView}>Verify & Ticket</button>
                    </div>
                  </div>
                  <div className={styles.tableRow}>
                    <span className={styles.cellId}>Ogun Tech Summit</span>
                    <span className={styles.cellType}><span className={styles.statusPill} style={{ background: '#6366f1' }}>Corporate</span></span>
                    <span className={styles.cellRegion}>Sagamu</span>
                    <span className={styles.cellType}>Nov 05, 2024</span>
                    <div className={styles.cellActions}>
                      <button className={styles.actionView}>Verify & Ticket</button>
                    </div>
                  </div>
                </div>
            </section>

            <div className={styles.intelligenceGrid}>
               <div className={styles.chartPlaceholder}>
                  <div className={styles.cardTitle}>LGA Development Progress</div>
                  <div className={styles.placeholderBox}>
                    <BarChart3 size={48} color="rgba(255,255,255,0.05)" />
                    <p>Real-time telemetry loading from API Node...</p>
                  </div>
               </div>
               <div className={styles.newsWidget}>
                  <div className={styles.cardTitle}>Ogun Signals (AI Crawler)</div>
                  <div className={styles.signalList}>
                     <div className={styles.signalItem}>
                        <div className={styles.signalDot} />
                        <p>Olumo CMS Update: New history digitized.</p>
                     </div>
                     <div className={styles.signalItem}>
                        <div className={styles.signalDot} color="#f59e0b" />
                        <p>Ojude Oba: High traffic predicted for Q3.</p>
                     </div>
                  </div>
               </div>
            </div>
          </>
        )}

        {activeTab === "kyc" && (
          <section className={styles.kycSection}>
            <div className={styles.kycTable}>
                <div className={styles.tableHeader}>
                  <span>Reference ID</span>
                  <span>Document</span>
                  <span>LGA Node</span>
                  <span>Status</span>
                  <span>Action</span>
                </div>
                {kycQueue.map(item => (
                  <div key={item.id} className={styles.tableRow}>
                    <span className={styles.cellId}>{item.id}</span>
                    <span className={styles.cellType}>{item.type}</span>
                    <span className={styles.cellRegion}>{item.region}</span>
                    <span className={`${styles.cellStatus} ${styles[item.status]}`}>{item.status}</span>
                    <div className={styles.cellActions}>
                      <button className={styles.actionView}>Review Node</button>
                      <ChevronRight size={16} />
                    </div>
                  </div>
                ))}
            </div>
            <div className={styles.kycSidebar}>
               <div className={styles.kycStatCard}>
                  <ShieldCheck size={24} color="#10b981" />
                  <div className={styles.kycStatLabel}>Auto-Verified (AI)</div>
                  <div className={styles.kycStatValue}>82%</div>
               </div>
            </div>
          </section>
        )}

        {activeTab === "lgas" && (
          <div className={styles.emptyState}>
            <Map size={48} color="rgba(255,255,255,0.05)" />
            <p>Geo-Intelligent Mapping Node initializing...</p>
          </div>
        )}
      </main>
    </div>
  );
}
