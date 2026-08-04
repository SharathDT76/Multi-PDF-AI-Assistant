function Header({ onMenuClick }) {

    return (

        <header className="app-header">

            <div className="app-header-left">

                <button className="menu-toggle" onClick={onMenuClick} aria-label="Toggle sidebar">
                    <span></span>
                </button>

                <div>
                    <div className="app-header-title">Chat with your library</div>
                    <div className="app-header-sub">ask a question, get an answer with receipts</div>
                </div>

            </div>

            <div className="header-badge">
                <span className="dot"></span>
                Knowledge base ready
            </div>

        </header>

    );

}

export default Header;
