import { FaUtensils } from "react-icons/fa";

function Navbar() {

    return (

        <header className="navbar">

            <div className="logo">

                <div className="logo-icon">
                    <FaUtensils />
                </div>

                <div className="logo-text">

                    <h1>
                        Royal<span>Feast</span>
                    </h1>

                </div>

            </div>

            <div className="navbar-quote">

                Order Smarter. Eat Better.

            </div>

        </header>

    );

}

export default Navbar;