import { Link } from "react-router";
import "./Footer.css";

export default function Footer() {
    return (
        <footer className="footer">
            <div className="footer-inner">
                <nav className="footer-links" aria-label="Footer">
                    <Link to="/contact" className="footer-link">Contact</Link>
                    <Link to="/privacy" className="footer-link">Privacy</Link>
                    <Link to="/terms" className="footer-link">terms</Link>
                </nav>
                <div className="footer-copy">Copyrights Reserved ©️ {new Date().getFullYear()}</div>
            </div>
        </footer>
    )
}