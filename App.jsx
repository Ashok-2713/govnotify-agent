import { useState } from "react";
import AdminDashboard from "./AdminDashboard";
import UserDashboard from "./UserDashboard";
const API_URL = "http://localhost:8080/api/auth";

const features = [
  ["🔍", "Smart Job Search", "Search jobs by qualification, department, state, category, and deadline."],
  ["🔔", "Instant Alerts", "Get alerts for new notifications, examination dates, and deadlines."],
  ["✓", "Eligibility Check", "Check eligibility based on your qualification, age, and category."],
  ["♡", "Save Jobs", "Save job notifications and review them whenever you are ready."],
  ["📄", "Official Links", "Access official notification PDFs and application links easily."],
  ["📅", "Exam Calendar", "Track application dates, admit cards, exams, and result notifications."]
];

const steps = [
  ["1", "Create Your Account", "Register with your basic details and preferred job categories."],
  ["2", "Find Suitable Jobs", "Search Central, State, Railway, Banking, Defence, and Teaching jobs."],
  ["3", "Track and Apply", "Save jobs, download notifications, and apply before the deadline."]
];

function App() {
  const [modal, setModal] = useState(null);
  const [loginMessage, setLoginMessage] = useState("");
  const [registerMessage, setRegisterMessage] = useState("");
  const [isAdmin, setIsAdmin] = useState(false);
  const [adminEmail, setAdminEmail] = useState("");
  const [isUser, setIsUser] = useState(false);
  const [userEmail, setUserEmail] = useState("");

  const openModal = (type) => {
    setModal(type);
    setLoginMessage("");
    setRegisterMessage("");
  };

  async function handleLogin(event) {
    event.preventDefault();

    const email = event.target.email.value.trim();
    const password = event.target.password.value;

    try {
      const response = await fetch(`${API_URL}/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password })
      });

      const data = await response.json();
      if (response.ok && data.role === "ADMIN") {
        setAdminEmail(data.email || email);
        setIsAdmin(true);
        return;
      }

      if (response.ok && (data.role === "USER" || response.ok)) {
        setUserEmail(data.email || email);
        setIsUser(true);
        return;
      }

      setLoginMessage(data.message || "Login failed. Please check your credentials.");
    } catch {
      setLoginMessage("Backend is not running. Start Spring Boot first.");
    }
  }

  async function handleRegister(event) {
    event.preventDefault();

    const fullName = event.target.fullName.value.trim();
    const email = event.target.email.value.trim();
    const password = event.target.password.value;

    try {
      const response = await fetch(`${API_URL}/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ fullName, email, password })
      });

      const data = await response.json();
      setRegisterMessage(data.message || "Registration completed.");

      if (response.ok) {
        event.target.reset();
      }
    } catch {
      setRegisterMessage("Backend is not running. Start Spring Boot first.");
    }
  }
  if (isAdmin) {
    return (
      <AdminDashboard
        adminEmail={adminEmail}
        onLogout={() => setIsAdmin(false)}
      />
    );
  }

  if (isUser) {
    return (
      <UserDashboard
        userEmail={userEmail}
        onLogout={() => setIsUser(false)}
      />
    );
  }
  return (
    <>
      <style>{styles}</style>

      <nav className="navbar">
        <div className="brand">
          <span className="brand-icon">⚖</span>
          GOV<span>NOTIFY</span>
        </div>

        <div className="nav-links">
          <a href="#home">Home</a>
          <a href="#features">Features</a>
          <a href="#how-it-works">How It Works</a>
          <a href="#about">About</a>
          <button className="login-btn" onClick={() => openModal("login")}>
            Login
          </button>
        </div>
      </nav>

      <section className="hero" id="home">
        <div className="hero-text">
          <h1>
            Government Jobs <span>Made Simple.</span>
          </h1>

          <p>
            Find Central and State Government job notifications in one place.
            Search jobs, save opportunities, and receive important deadline alerts.
          </p>

          <div className="hero-buttons">
            <button className="primary-btn" onClick={() => openModal("register")}>
              Create Free Account
            </button>

            <a className="secondary-btn" href="#features">
              Explore Features
            </a>
          </div>
        </div>

        <div className="hero-image">
          <img
            src="https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1200&q=85"
            alt="Students studying together"
          />
          <div className="hero-badge">New Government Job Alerts Daily</div>
        </div>
      </section>

      <section className="section" id="features">
        <h2 className="section-title">
          Why Choose <span>GovNotify?</span>
        </h2>

        <p className="section-description">
          A single portal to search, save, and track suitable government job opportunities.
        </p>

        <div className="features-grid">
          {features.map(([icon, title, text]) => (
            <article className="feature-card" key={title}>
              <div className="feature-icon">{icon}</div>
              <h3>{title}</h3>
              <p>{text}</p>
            </article>
          ))}
        </div>
      </section>

      <section className="section how-it-works" id="how-it-works">
        <h2 className="section-title">
          How It <span>Works</span>
        </h2>

        <p className="section-description">
          Start finding relevant government job opportunities in three simple steps.
        </p>

        <div className="steps">
          {steps.map(([number, title, text]) => (
            <div className="step" key={number}>
              <div className="step-number">{number}</div>
              <h3>{title}</h3>
              <p>{text}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="section about" id="about">
        <img
          src="https://images.unsplash.com/photo-1498243691581-b145c3f54a5a?auto=format&fit=crop&w=1200&q=85"
          alt="Student preparing for an exam"
        />

        <div className="about-text">
          <h2>
            Your Career Journey <span>Starts Here.</span>
          </h2>

          <p>
            GovNotify is a Government Job Notification Portal created to make
            searching and tracking government job opportunities easier for aspirants.
          </p>

          <ul className="about-points">
            <li>Central and State government job information</li>
            <li>Easy qualification-based job filters</li>
            <li>Saved jobs and application tracking</li>
            <li>Exam and deadline notifications</li>
          </ul>

          <button className="primary-btn" onClick={() => openModal("register")}>
            Start Exploring Jobs
          </button>
        </div>
      </section>

      <section className="cta">
        <h2>Ready to Find Your Government Job?</h2>
        <p>Create your free GovNotify account and never miss an opportunity.</p>
        <button onClick={() => openModal("register")}>Create Account</button>
      </section>

      <footer>
        <div><strong>GOVNOTIFY</strong> — Government Job Notification Portal</div>
        <div>© 2026 GovNotify. Academic Project.</div>
      </footer>

      {modal === "login" && (
        <div className="modal" onClick={() => setModal(null)}>
          <div className="modal-box" onClick={(event) => event.stopPropagation()}>
            <button className="close-btn" onClick={() => setModal(null)}>×</button>

            <h2>Welcome Back</h2>
            <p className="modal-description">
              Log in to access your saved jobs and alerts.
            </p>

            <form onSubmit={handleLogin}>
              <label>Email Address</label>
              <input name="email" type="email" placeholder="Enter your email" required />

              <label>Password</label>
              <input name="password" type="password" placeholder="Enter your password" required />

              <button type="submit" className="primary-btn">Login</button>

              {loginMessage && <p className="form-message">{loginMessage}</p>}
            </form>
          </div>
        </div>
      )}

      {modal === "register" && (
        <div className="modal" onClick={() => setModal(null)}>
          <div className="modal-box" onClick={(event) => event.stopPropagation()}>
            <button className="close-btn" onClick={() => setModal(null)}>×</button>

            <h2>Create Your Account</h2>
            <p className="modal-description">
              Register to receive job updates and alerts.
            </p>

            <form onSubmit={handleRegister}>
              <label>Full Name</label>
              <input name="fullName" type="text" placeholder="Enter your full name" required />

              <label>Email Address</label>
              <input name="email" type="email" placeholder="Enter your email" required />

              <label>Password</label>
              <input
                name="password"
                type="password"
                placeholder="Minimum 8 characters"
                minLength="8"
                required
              />

              <button type="submit" className="primary-btn">Create Account</button>

              {registerMessage && <p className="form-message">{registerMessage}</p>}
            </form>
          </div>
        </div>
      )}
    </>
  );
}

const styles = `
  :root {
    --dark: #071a2d;
    --dark-card: #102a43;
    --teal: #19d3c5;
    --teal-light: #7cf7e9;
    --purple: #7c3aed;
    --blue: #2563eb;
    --white: #f5fbff;
    --muted: #a9c0d4;
    --line: #1f4e65;
  }

  * {
    box-sizing: border-box;
    scroll-behavior: smooth;
  }

  body {
    margin: 0;
    background: var(--dark);
    color: var(--white);
    font-family: Arial, sans-serif;
  }

  #root {
    width: 100%;
    min-height: 100vh;
    max-width: none;
    margin: 0;
    padding: 0;
  }

  button, input {
    font: inherit;
  }

  .navbar {
    height: 76px;
    padding: 0 8%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(7, 26, 45, .97);
    border-bottom: 1px solid var(--line);
    position: sticky;
    top: 0;
    z-index: 10;
  }

  .brand {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 22px;
    font-weight: bold;
  }

  .brand-icon {
    color: var(--teal);
    font-size: 28px;
  }

  .brand span {
    color: var(--teal);
  }

  .nav-links {
    display: flex;
    align-items: center;
    gap: 25px;
  }

  .nav-links a {
    color: var(--white);
    text-decoration: none;
    font-size: 14px;
  }

  .nav-links a:hover {
    color: var(--teal);
  }

  .login-btn, .primary-btn {
    background: var(--teal);
    color: #071a2d;
    border: none;
    border-radius: 7px;
    padding: 12px 20px;
    font-weight: bold;
    cursor: pointer;
  }

  .login-btn:hover, .primary-btn:hover {
    background: var(--teal-light);
  }

  .hero {
    min-height: 600px;
    padding: 80px 8%;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 50px;
    align-items: center;
    background:
      radial-gradient(circle at top left, #173d67 0%, transparent 38%),
      radial-gradient(circle at bottom right, #3e1d70 0%, transparent 35%),
      var(--dark);
  }

  .hero-text h1 {
    margin: 0 0 20px;
    font-size: clamp(42px, 5vw, 68px);
    line-height: 1.1;
  }

  .hero-text h1 span, .section-title span, .about-text h2 span {
    color: var(--teal);
  }

  .hero-text p {
    max-width: 560px;
    color: var(--muted);
    font-size: 17px;
    line-height: 1.8;
  }

  .hero-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 14px;
    margin-top: 30px;
  }

  .secondary-btn {
    padding: 12px 20px;
    border: 1px solid var(--teal);
    border-radius: 7px;
    background: transparent;
    color: var(--white);
    text-decoration: none;
    font-weight: bold;
    cursor: pointer;
  }

  .secondary-btn:hover {
    background: var(--teal);
    color: var(--dark);
  }

  .hero-image {
    position: relative;
  }

  .hero-image img {
    width: 100%;
    height: 430px;
    border-radius: 20px;
    object-fit: cover;
    box-shadow: 0 15px 40px rgba(0, 0, 0, .45);
  }

  .hero-badge {
    position: absolute;
    bottom: -20px;
    left: -20px;
    padding: 17px 20px;
    border-radius: 12px;
    background: linear-gradient(135deg, var(--purple), var(--teal));
    color: white;
    font-weight: bold;
    box-shadow: 0 10px 25px rgba(0, 0, 0, .35);
  }

  .section {
    padding: 90px 8%;
  }

  .section-title {
    margin: 0;
    text-align: center;
    font-size: 38px;
  }

  .section-description {
    max-width: 680px;
    margin: 15px auto 45px;
    text-align: center;
    color: var(--muted);
    line-height: 1.7;
  }

  .features-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
  }

  .feature-card {
    padding: 27px;
    border: 1px solid var(--line);
    border-radius: 14px;
    background: var(--dark-card);
    transition: .25s;
  }

  .feature-card:hover {
    transform: translateY(-7px);
    border-color: var(--teal);
    box-shadow: 0 10px 25px rgba(25, 211, 197, .15);
  }

  .feature-icon {
    width: 50px;
    height: 50px;
    display: grid;
    place-items: center;
    border-radius: 12px;
    background: linear-gradient(135deg, var(--purple), var(--teal));
    font-size: 22px;
  }

  .feature-card h3 {
    margin: 18px 0 10px;
  }

  .feature-card p, .step p {
    margin: 0;
    color: var(--muted);
    font-size: 14px;
    line-height: 1.7;
  }

  .how-it-works {
    background: linear-gradient(135deg, #0c2238, #13234e);
  }

  .steps {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 30px;
    max-width: 1050px;
    margin: auto;
  }

  .step {
    text-align: center;
  }

  .step-number {
    width: 54px;
    height: 54px;
    display: grid;
    place-items: center;
    margin: auto;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--purple), var(--teal));
    font-size: 20px;
    font-weight: bold;
  }

  .step h3 {
    margin: 18px 0 10px;
  }

  .about {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 50px;
    align-items: center;
  }

  .about img {
    width: 100%;
    height: 360px;
    border-radius: 16px;
    object-fit: cover;
  }

  .about-text h2 {
    margin: 0 0 18px;
    font-size: 38px;
  }

  .about-text p {
    color: var(--muted);
    line-height: 1.8;
  }

  .about-points {
    padding: 0;
    list-style: none;
    line-height: 2.3;
  }

  .about-points li::before {
    content: "✓";
    margin-right: 10px;
    color: var(--teal);
    font-weight: bold;
  }

  .cta {
    padding: 75px 8%;
    text-align: center;
    background: linear-gradient(120deg, var(--purple), var(--blue), var(--teal));
    color: white;
  }

  .cta h2 {
    margin: 0;
    font-size: 38px;
  }

  .cta p {
    margin: 15px 0 25px;
  }

  .cta button {
    padding: 14px 25px;
    border: none;
    border-radius: 7px;
    background: var(--dark);
    color: white;
    font-weight: bold;
    cursor: pointer;
  }

  footer {
    padding: 40px 8%;
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 20px;
    background: #040d18;
    color: var(--muted);
    font-size: 14px;
  }

  .modal {
    position: fixed;
    inset: 0;
    z-index: 50;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
    background: rgba(0, 0, 0, .75);
  }

  .modal-box {
    position: relative;
    width: 100%;
    max-width: 420px;
    padding: 32px;
    border: 1px solid var(--line);
    border-radius: 15px;
    background: var(--dark-card);
  }

  .close-btn {
    position: absolute;
    top: 12px;
    right: 17px;
    border: none;
    background: none;
    color: white;
    font-size: 25px;
    cursor: pointer;
  }

  .modal-description {
    color: var(--muted);
  }

  .modal-box label {
    display: block;
    margin-top: 15px;
    font-size: 14px;
  }

  .modal-box input {
    width: 100%;
    margin-top: 7px;
    padding: 12px;
    border: 1px solid var(--line);
    border-radius: 7px;
    outline: none;
    background: #081725;
    color: white;
  }

  .modal-box input:focus {
    border-color: var(--teal);
  }

  .modal-box button[type="submit"] {
    width: 100%;
    margin-top: 24px;
  }

  .form-message {
    margin: 15px 0 0;
    padding: 10px;
    border-radius: 7px;
    background: #203e57;
    color: white;
    font-size: 14px;
  }

  @media (max-width: 850px) {
    .hero, .about, .features-grid, .steps {
      grid-template-columns: 1fr;
    }

    .nav-links a {
      display: none;
    }

    .hero {
      padding-top: 50px;
    }

    .hero-badge {
      left: 10px;
    }
  }
`;

export default App;