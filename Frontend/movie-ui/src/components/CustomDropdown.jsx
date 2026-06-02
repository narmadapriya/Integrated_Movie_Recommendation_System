import React, {
  useState,
  useRef,
  useEffect,
} from "react";

import {
  ChevronDown,
  ChevronUp,
  Check,
} from "lucide-react";

const CustomDropdown = ({
  options = [],
  selected,
  setSelected,
  placeholder,
}) => {
  const [isOpen, setIsOpen] =
    useState(false);

  const [searchTerm, setSearchTerm] =
    useState("");

  const dropdownRef = useRef(null);

  // ==================================================
  // CLOSE DROPDOWN WHEN CLICK OUTSIDE
  // ==================================================

  useEffect(() => {
    const handleClickOutside = (
      event
    ) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(
          event.target
        )
      ) {
        setIsOpen(false);

        setSearchTerm("");
      }
    };

    document.addEventListener(
      "mousedown",
      handleClickOutside
    );

    return () => {
      document.removeEventListener(
        "mousedown",
        handleClickOutside
      );
    };
  }, []);

  // ==================================================
  // FILTER OPTIONS
  // ==================================================

  const filteredOptions =
    searchTerm.trim() === ""
      ? []
      : options.filter((option) =>
          option
            ?.toLowerCase()
            .includes(
              searchTerm.toLowerCase()
            )
        );

  // ==================================================
  // HANDLE SELECT
  // ==================================================

  const handleSelect = (option) => {
    setSelected(option);

    setSearchTerm(option);

    setIsOpen(false);
  };

  // ==================================================
  // HANDLE INPUT CHANGE
  // ==================================================

  const handleInputChange = (e) => {
    const value = e.target.value;

    setSearchTerm(value);

    setSelected(value);

    if (value.trim() !== "") {
      setIsOpen(true);
    } else {
      setIsOpen(false);
    }
  };

  return (
    <div
      className="filter-field-wrapper"
      ref={dropdownRef}
    >
      {/* TYPEHEAD INPUT */}

      <div
        className={`filter-input-container ${
          isOpen ? "active" : ""
        }`}
      >
        <input
          type="text"
          className="filter-input"
          placeholder={placeholder}
          value={
            searchTerm || selected || ""
          }
          onChange={handleInputChange}
          onFocus={() => {
            if (
              searchTerm.trim() !== ""
            ) {
              setIsOpen(true);
            }
          }}
        />

        {/* DROPDOWN ICON */}

        <div className="dropdown-toggle-btn">
          {isOpen ? (
            <ChevronUp size={18} />
          ) : (
            <ChevronDown size={18} />
          )}
        </div>
      </div>

      {/* DROPDOWN RESULTS */}

      {isOpen && (
        <div className="dropdown-panel">
          <div className="dropdown-scroll-area">
            {filteredOptions.length >
            0 ? (
              filteredOptions.map(
                (option) => (
                  <button
                    key={option}
                    type="button"
                    className={`dropdown-item ${
                      selected ===
                      option
                        ? "active"
                        : ""
                    }`}
                    onClick={() =>
                      handleSelect(
                        option
                      )
                    }
                  >
                    <span>
                      {option}
                    </span>

                    {selected ===
                      option && (
                      <Check
                        size={15}
                        className="check-icon"
                      />
                    )}
                  </button>
                )
              )
            ) : (
              <div className="no-results">
                No results found
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default CustomDropdown;