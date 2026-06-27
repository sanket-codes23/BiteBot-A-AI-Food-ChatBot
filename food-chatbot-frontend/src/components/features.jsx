import { FaRobot, FaTruck, FaCreditCard, FaLeaf } from "react-icons/fa";

function Features() {

    const features = [

        {
            icon: <FaRobot />,
            title: "AI Ordering",
            text: "Chat naturally with BiteBot to place your food order."
        },

        {
            icon: <FaTruck />,
            title: "Live Tracking",
            text: "Track your order in real-time until it reaches your doorstep."
        },

        {
            icon: <FaCreditCard />,
            title: "Secure Payment",
            text: "Safe and reliable payment options for every customer."
        },

        {
            icon: <FaLeaf />,
            title: "Fresh Food",
            text: "Prepared with fresh ingredients and delivered hot."
        }

    ];

    return (

        <section className="features" id="features">

            <h2>✨ Why Choose RoyalFeast?</h2>

            <div className="feature-grid">

                {

                    features.map((feature,index)=>(

                        <div className="feature-card" key={index}>

                            <div className="icon">

                                {feature.icon}

                            </div>

                            <h3>{feature.title}</h3>

                            <p>{feature.text}</p>

                        </div>

                    ))

                }

            </div>

        </section>

    );

}

export default Features;