CREATE OR REPLACE FUNCTION bucketize_1(input_num NUMERIC, b_size NUMERIC)
RETURNS NUMRANGE
AS $$
DECLARE
    lower_bound NUMERIC;
    upper_bound NUMERIC;
BEGIN
    IF input_num < 0.0 THEN
        upper_bound := input_num - (input_num % b_size);
        lower_bound := input_num - b_size - (input_num % b_size);
    ELSE 
        lower_bound := input_num - (input_num % b_size);
        upper_bound := input_num + b_size - (input_num % b_size);
    END IF;
    RETURN NUMRANGE(lower_bound + 1.0, upper_bound + 1.0);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION bucketize_1_low(input_num NUMERIC, b_size NUMERIC)
RETURNS NUMERIC
AS $$
BEGIN
    IF input_num < 0.0 THEN
        RETURN input_num - b_size - (input_num % b_size) + 1.0;
    ELSE 
        RETURN input_num - (input_num % b_size) + 1.0;
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION noise_cow(original_number NUMERIC, probability NUMERIC)
RETURNS NUMERIC AS $$
DECLARE
    random_number NUMERIC;
BEGIN
    -- Check if the probability is within the valid range
    IF probability < 0.0 OR probability > 1.0 THEN
        RAISE EXCEPTION 'Probability must be between 0 and 1';
    END IF;

    -- Check if the original number should be changed based on the probability
    IF random() < probability THEN
		random_number := floor(random() * 8.0) + 1.0;
        RETURN round(random_number, 1);
    ELSE
        RETURN original_number;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION noise_mar(original_number NUMERIC, probability NUMERIC)
RETURNS NUMERIC AS $$
DECLARE
    random_number NUMERIC;
BEGIN
    -- Check if the probability is within the valid range
    IF probability < 0.0 OR probability > 1.0 THEN
        RAISE EXCEPTION 'Probability must be between 0 and 1';
    END IF;

    -- Check if the original number should be changed based on the probability
    IF random() < probability THEN
		random_number := floor(random() * 5.0) + 1.0;
        RETURN round(random_number, 1);
    ELSE
        RETURN original_number;
    END IF;
END;
$$ LANGUAGE plpgsql;