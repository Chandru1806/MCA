export interface Preference {
  profile_id: string;
  first_name: string;
  last_name: string;
  username: string;
  email: string;
  phone: string | null;
  address_line_1: string | null;
  address_line_2: string | null;
  city: string | null;
  state: string | null;
  created_at: string;
  updated_at: string;
  is_active: string;
}

export interface PreferenceFormData {
  phone: string;
  address_line_1: string;
  address_line_2: string;
  city: string;
  state: string;
}
