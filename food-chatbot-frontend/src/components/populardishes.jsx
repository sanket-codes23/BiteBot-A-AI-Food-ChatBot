import pizza from "../assets/pizza.png";
import burger from "../assets/burger.png";
import pasta from "../assets/pasta.png";
import coffee from "../assets/coffee.png";
import cake from "../assets/cake.jpg";
import dosa from "../assets/rava_dosa.jpg";

function PopularDishes() {

    const dishes=[

        {
            image:pizza,
            name:"Margherita Pizza",
            price:"₹299"
        },

        {
            image:burger,
            name:"Cheese Burger",
            price:"₹249"
        },

        {
            image:pasta,
            name:"White Sauce Pasta",
            price:"₹279"
        },

        {
            image:dosa,
            name:"rava dosa",
            price:"₹349"
        },

        {
            image:coffee,
            name:"Cold Coffee",
            price:"₹129"
        },

        {
            image:cake,
            name:"Chocolate Cake",
            price:"₹199"
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

                    dishes.map((dish,index)=>(

                        <div
                            className="food-card"
                            key={index}
                        >

                            <img
                                src={dish.image}
                                alt={dish.name}
                            />

                            <div className="food-info">

                                <h3>

                                    {dish.name}

                                </h3>

                                <p
                                    className="price"
                                >

                                    {dish.price}

                                </p>

                                <p
                                    className="rating"
                                >

                                    ★★★★★

                                </p>

                                <button>

                                    Order Now

                                </button>

                            </div>

                        </div>

                    ))

                }

            </div>

        </section>

    );

}

export default PopularDishes;