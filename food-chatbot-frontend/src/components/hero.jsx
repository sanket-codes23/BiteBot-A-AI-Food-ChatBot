
import backgroundImage from "../assets/background_image.png";

function Hero() {

    const scrollToMenu = () => {

        document
            .getElementById("menu")
            ?.scrollIntoView({
                behavior: "smooth"
            });

    };

    return (

        <section
            className="hero"
            id="home"
            style={{
                backgroundImage: `linear-gradient(
                    rgba(255,255,255,0.55),
                    rgba(255,255,255,0.55)
                ), url(${backgroundImage})`
            }}
        >

            <div className="hero-left">

                <h5>
                    🍽 INDIA'S SMART FOOD DELIVERY
                </h5>

                <h1>

                    Delicious Food,
                    <br />
                    Delivered Faster

                </h1>

                <p>

                    Welcome to <strong>RoyalFeast</strong>.

                    Discover a smarter way to enjoy your favourite meals with
                    our AI-powered assistant <strong>BiteBot</strong>.

                    Browse the menu, customize your order, track deliveries
                    in real time and enjoy fresh food delivered straight to
                    your doorstep.

                </p>

                <div className="hero-buttons">

                    <button
                        className="primary-btn"
                        onClick={scrollToMenu}
                    >
                        🍔 Order Now
                    </button>

                </div>

            </div>

        </section>

    );

}

export default Hero;
