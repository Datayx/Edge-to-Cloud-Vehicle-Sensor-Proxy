export function VehicleSelector({ vehicles, selected, onSelect }) {
    return (
        <div>
            {vehicles.map(id => (
                <button
                    key={id}
                    onClick={() => onSelect(id)}
                    style={{ fontWeight: selected === id ? "bold" : "normal", margin: 4 }}
                >
                    {id}
                </button>
            ))}
        </div>
    );
}