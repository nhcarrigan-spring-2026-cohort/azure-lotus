import './Input.css';

export default function Input({
  id,
  name,
  type = 'text',
  placeholder,
  value,
  onChange,
  error = '',
  ...rest
}) {
  return (
    <div className="input-container">
      <input
        id={id}
        name={name}
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        className={error ? 'input-field errored' : 'input-field'}
        {...rest}
      />
      {error && <span className="error-text">{error}</span>}
    </div>
  );
}
