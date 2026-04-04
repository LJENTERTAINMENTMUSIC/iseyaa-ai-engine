"use client";

import { useState } from "react";
import { 
  Store, Tent, MapPin, MessageSquare, 
  Settings, User, PlusCircle, CreditCard,
  ChevronRight, Star, Clock, Package
} from "lucide-react";
import styles from "./page.module.css";

export default function HostDashboard() {
  const [activeTab, setActiveTab] = useState("listings");

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
                  <p className={styles.listingMeta}>$25.00 · Heritage Guide</p>
                </div>
                <ChevronRight size={16} color="#475569" />
              </div>
              <div className={styles.listingItem}>
                <div className={styles.listingImg} style={{ background: "#064e3b" }}>🏨</div>
                <div className={styles.listingInfo}>
                  <p className={styles.listingName}>Forest Edge Eco-Lodge</p>
                  <p className={styles.listingMeta}>$85.00 · Stay</p>
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
              <div className={styles.earningsVal}>$1,240.50</div>
              <p className={styles.earningsSub}>+12% from last month</p>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}
