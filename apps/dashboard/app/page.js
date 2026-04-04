"use client";

import { useState, useEffect } from "react";
import { 
  BarChart3, LayoutDashboard, Map, Calendar, 
  Settings, User, LogOut, ArrowLeftRight, 
  Activity, Users, Globe, ShieldCheck
} from "lucide-react";
import styles from "./page.module.css";

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState("overview");

  return (
    <div className={styles.container}>
      {/* Sidebar */}
      <aside className={styles.sidebar}>
        <div className={styles.brand}>
          <div className={styles.logo}>🌿</div>
          <div>
            <h1 className={styles.brandName}>ISEYAA</h1>
            <p className={styles.brandTag}>Gov Command Center</p>
          </div>
        </div>

        <nav className={styles.nav}>
          <div className={styles.navSection}>Analytics</div>
          <button className={`${styles.navItem} ${activeTab === "overview" ? styles.active : ""}`} onClick={() => setActiveTab("overview")}>
            <LayoutDashboard size={18} /> Overview
          </button>
          <button className={`${styles.navItem} ${activeTab === "revenue" ? styles.active : ""}`} onClick={() => setActiveTab("revenue")}>
            <BarChart3 size={18} /> LGA Revenue
          </button>
          
          <div className={styles.navSection}>Governance</div>
          <button className={`${styles.navItem}`}>
            <Map size={18} /> LGA Intelligence
          </button>
          <button className={`${styles.navItem}`}>
            <ShieldCheck size={18} /> Compliance
          </button>
        </nav>

        <div className={styles.sidebarFooter}>
          <div className={styles.profile}>
            <div className={styles.avatar}>GO</div>
            <div>
              <p className={styles.userName}>Gov Official</p>
              <p className={styles.userRole}>Abeokuta South</p>
            </div>
          </div>
          
          {/* Switcher */}
          <div className={styles.switcherBlock}>
            <p className={styles.switcherLabel}>Profile Mode</p>
            <div className={styles.switcher}>
              <button className={styles.switchBtn} onClick={() => window.location.href='http://localhost:3000'}>Traveler</button>
              <button className={styles.switchBtn} onClick={() => window.location.href='http://localhost:3002'}>Host</button>
              <button className={`${styles.switchBtn} ${styles.switchBtnActive}`}>Govt</button>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className={styles.main}>
        <header className={styles.header}>
          <div>
            <h2 className={styles.pageTitle}>State Overview</h2>
            <p className={styles.pageSub}>Real-time economic & cultural diagnostics for Ogun State.</p>
          </div>
          <div className={styles.headerActions}>
            <div className={styles.uptime}>● Engine Online</div>
            <button className={styles.profileBtn}><User size={20} /></button>
          </div>
        </header>

        <section className={styles.grid}>
          <div className={styles.statCard}>
            <Activity className={styles.statIcon} color="#10b981" />
            <div className={styles.statValue}>3.2M</div>
            <div className={styles.statLabel}>Monthly Visitors</div>
          </div>
          <div className={styles.statCard}>
            <Users className={styles.statIcon} color="#6366f1" />
            <div className={styles.statValue}>842</div>
            <div className={styles.statLabel}>Active Artisans</div>
          </div>
          <div className={styles.statCard}>
            <Globe className={styles.statIcon} color="#f59e0b" />
            <div className={styles.statValue}>20</div>
            <div className={styles.statLabel}>Digitized LGAs</div>
          </div>
        </section>

        <section className={styles.chartPlaceholder}>
          <div className={styles.placeholderBox}>
            <BarChart3 size={48} color="rgba(255,255,255,0.1)" />
            <p>Intelligence Graphs Loading...</p>
          </div>
        </section>
      </main>
    </div>
  );
}
