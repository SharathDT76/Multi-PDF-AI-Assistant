const SPINE_COLORS = ["#b8863e", "#3a6b63", "#8a5a44", "#5c7a8a", "#9a7b3f", "#4f6b5a"];

function fileExt(name = "") {
    const parts = name.split(".");
    return parts.length > 1 ? parts[parts.length - 1].toUpperCase() : "FILE";
}

function Sidebar({ files, isOpen, onClose, onReset }) {

    return (
        <>
            <div
                className={`sidebar-backdrop ${isOpen ? "open" : ""}`}
                onClick={onClose}
            />

            <aside className={`sidebar ${isOpen ? "open" : ""}`}>

                <div className="sidebar-brand">
                    <div className="sidebar-brand-mark">Marginalia</div>
                    <div className="sidebar-brand-tag">notes in the margins of your PDFs</div>
                </div>

                <div className="sidebar-section-label">
                    Your shelf ({files.length})
                </div>

                <div className="shelf">
                    {
                        files.length === 0 ? (
                            <div className="shelf-empty">
                                No documents indexed yet.
                            </div>
                        ) : (
                            files.map((file, index) => (
                                <div className="spine" key={index}>
                                    <div
                                        className="spine-bar"
                                        style={{ background: SPINE_COLORS[index % SPINE_COLORS.length] }}
                                    />
                                    <div>
                                        <div className="spine-name">{file.name}</div>
                                        <div className="spine-meta">{fileExt(file.name)}</div>
                                    </div>
                                </div>
                            ))
                        )
                    }
                </div>

                <div className="sidebar-footer">
                    <button className="sidebar-reset" onClick={onReset}>
                        ↺ Start a new library
                    </button>
                </div>

            </aside>
        </>
    );

}

export default Sidebar;
