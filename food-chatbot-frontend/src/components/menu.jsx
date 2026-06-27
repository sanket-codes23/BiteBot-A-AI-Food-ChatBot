import {
    FaPizzaSlice,
    FaHamburger,
    FaIceCream,
    FaCoffee,
    FaDrumstickBite,
    FaGlassWhiskey
} from "react-icons/fa";

function Menu() {

    const foods = [

        {
            icon: <FaPizzaSlice />,
            name: "Margherita Pizza",
            price: "₹299",
            rating: "★★★★★"
        },

        {
            icon: <FaHamburger />,
            name: "Cheese Burger",
            price: "₹249",
            rating: "★★★★★"
        },

        {
            icon: <FaDrumstickBite />,
            name: "Chicken Wings",
            price: "₹349",
            rating: "★★★★☆"
        },

        {
            icon: <FaIceCream />,
            name: "Chocolate Ice Cream",
            price: "₹149",
            rating: "★★★★★"
        },

        {
            icon: <FaCoffee />,
            name: "Cold Coffee",
            price: "₹129",
            rating: "★★★★☆"
        },

        {
            icon: <FaGlassWhiskey />,
            name: "Fresh Juice",
            price: "₹99",
            rating: "★★★★★"
        }

    ];

    return (

        <section
            className="menu"
            id="menu"
        >

            <h2>

                🍽 Popular Dishes

            </h2>

            <div className="menu-grid">

                {

                    foods.map((food,index)=>(

                        <div
                            className="food-card"
                            key={index}
                        >

                            <div className="food-icon">

                                {food.icon}

                            </div>

                            <h3>

                                {food.name}

                            </h3>

                            <h4>

                                {food.price}

                            </h4>

                            <p>

                                {food.rating}

                            </p>

                            <button>

                                Order Now

                            </button>

                        </div>

                    ))

                }

            </div>

        </section>

    );

}

export default Menu;