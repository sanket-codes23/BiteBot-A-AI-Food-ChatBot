function Chatbot() {

    return (

        <div className="chatbot-wrapper">

            <div className="chatbot-label">
                💬 Chat with BiteBot
            </div>

            <df-messenger
                intent="WELCOME"
                chat-title="BiteBot"
                agent-id="10f3b77d-4de4-4d80-81a3-67582948da5b"
                language-code="en"
            ></df-messenger>

        </div>

    );

}

export default Chatbot;