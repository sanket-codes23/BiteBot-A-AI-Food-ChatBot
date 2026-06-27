import {
    FaGithub,
    FaLinkedin,
    FaEnvelope,
    FaRobot,
    FaUtensils
} from "react-icons/fa";

function Footer() {

    return (

        <footer className="footer" id="footer">

            <div className="footer-container">

                <div className="footer-left">

                    <h2>
                        <FaUtensils /> RoyalFeast
                    </h2>

                    <p>

                        Experience AI-powered food ordering with
                        <strong> BiteBot</strong>.

                    </p>

                    
                </div>

                <div className="footer-middle">

                    <h3>Features</h3>

                    <ul>

                        <li>🍔 AI Food Ordering</li>

                        <li>📦 Live Order Tracking</li>

                        <li>💳 Secure Payments</li>

                        <li>⭐ Fresh & Quality Food</li>

                    </ul>

                </div>

                <div className="footer-right">

                    <h3>Connect</h3>

                    <div className="social-icons">

                        <a href="#">
                            <FaGithub />
                        </a>

                        <a href="#">
                            <FaLinkedin />
                        </a>

                        <a href="#">
                            <FaEnvelope />
                        </a>

                        <a href="#chatbot">
                            <FaRobot />
                        </a>

                    </div>

                </div>

            </div>

            <hr />

            <div className="copyright">

                © 2026 RoyalFeast | AI Powered Food Ordering System

            </div>

        </footer>

    );

}

export default Footer;