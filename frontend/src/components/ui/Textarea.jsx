import styles from "./Textarea.module.css";
import React, { forwardRef, useId } from "react";
import PropTypes from "prop-types";

const Textarea = forwardRef(
  (
    {
      size = "medium",
      className = "",
      wrapperClassName = "",
      errorClassName = "",
      error = "",
      ...props
    },
    ref,
  ) => {
    const errorId = useId();

    const wrapperClasses = [styles.wrapper, wrapperClassName]
      .filter(Boolean)
      .join(" ");

    const textareaClasses = [
      styles.textarea,
      styles[`textarea-${size}`],
      className,
      error ? styles.errored : "",
    ]
      .filter(Boolean)
      .join(" ");

    const errorClasses = [styles.errorText, errorClassName]
      .filter(Boolean)
      .join(" ");

    return (
      <div className={wrapperClasses}>
        <textarea
          ref={ref}
          className={textareaClasses}
          aria-invalid={!!error}
          aria-describedby={error ? errorId : undefined}
          {...props}
        />
        {error && (
          <span id={errorId} className={errorClasses} role="alert">
            {error}
          </span>
        )}
      </div>
    );
  },
);

Textarea.displayName = "Textarea";

Textarea.propTypes = {
  size: PropTypes.oneOf(["small", "medium", "large"]),
  className: PropTypes.string,
  wrapperClassName: PropTypes.string,
  errorClassName: PropTypes.string,
  error: PropTypes.string,
};

export default Textarea;
