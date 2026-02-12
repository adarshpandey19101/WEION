-- Enable UUID extension
create extension if not exists "uuid-ossp";

-- PROFILES: Public user data linked to auth.users
create table public.profiles (
  id uuid references auth.users not null primary key,
  email text,
  full_name text,
  avatar_url text,
  role text default 'member',
  created_at timestamptz default now()
);

-- RLS for Profiles
alter table public.profiles enable row level security;

create policy "Public profiles are viewable by everyone"
  on public.profiles for select
  using ( true );

create policy "Users can insert their own profile"
  on public.profiles for insert
  with check ( auth.uid() = id );

create policy "Users can update their own profile"
  on public.profiles for update
  using ( auth.uid() = id );

-- MISSIONS: High-level goals/tasks
create table public.missions (
  id uuid default uuid_generate_v4() primary key,
  user_id uuid references public.profiles(id) not null,
  title text not null,
  description text,
  priority text default 'medium', -- low, medium, high
  status text default 'active', -- active, completed, failed, paused
  progress integer default 0,
  cognitive_load integer default 0,
  created_at timestamptz default now()
);

-- RLS for Missions
alter table public.missions enable row level security;

create policy "Users can view their own missions"
  on public.missions for select
  using ( auth.uid() = user_id );

create policy "Users can insert their own missions"
  on public.missions for insert
  with check ( auth.uid() = user_id );

create policy "Users can update their own missions"
  on public.missions for update
  using ( auth.uid() = user_id );

create policy "Users can delete their own missions"
  on public.missions for delete
  using ( auth.uid() = user_id );

-- CHATS: Conversation threads
create table public.chats (
  id uuid default uuid_generate_v4() primary key,
  user_id uuid references public.profiles(id) not null,
  title text,
  project_id uuid references public.projects(id) on delete set null,
  created_at timestamptz default now()
);

-- RLS for Chats
alter table public.chats enable row level security;

create policy "Users can view their own chats"
  on public.chats for select
  using ( auth.uid() = user_id );

create policy "Users can insert their own chats"
  on public.chats for insert
  with check ( auth.uid() = user_id );

create policy "Users can update their own chats"
  on public.chats for update
  using ( auth.uid() = user_id );

create policy "Users can delete their own chats"
  on public.chats for delete
  using ( auth.uid() = user_id );

-- MESSAGES: Individual messages in a chat
create table public.messages (
  id uuid default uuid_generate_v4() primary key,
  chat_id uuid references public.chats(id) on delete cascade not null,
  role text not null, -- 'user' or 'ai'
  content text not null,
  created_at timestamptz default now()
);

-- RLS for Messages
alter table public.messages enable row level security;

-- Policy to view messages: The user must own the chat that the message belongs to
create policy "Users can view messages in their own chats"
  on public.messages for select
  using (
    exists (
      select 1 from public.chats
      where public.chats.id = public.messages.chat_id
      and public.chats.user_id = auth.uid()
    )
  );

create policy "Users can insert messages in their own chats"
  on public.messages for insert
  with check (
    exists (
      select 1 from public.chats
      where public.chats.id = public.messages.chat_id
      and public.chats.user_id = auth.uid()
    )
  );

-- Function to handle new user signup (Trigger)
-- This automatically creates a profile entry when a new user signs up
create or replace function public.handle_new_user()
returns trigger as $$
begin
  insert into public.profiles (id, email, full_name, avatar_url)
  values (new.id, new.email, new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'avatar_url');
  return new;
end;
$$ language plpgsql security definer;

-- Trigger for new user signup
create or replace trigger on_auth_user_created
  after insert on auth.users
  for each row execute procedure public.handle_new_user();

-- =============================================
-- PROJECTS: Folder organization for chats/missions
-- =============================================
create table public.projects (
  id uuid default uuid_generate_v4() primary key,
  user_id uuid references public.profiles(id) on delete cascade not null,
  name text not null,
  description text,
  color text default '#3b82f6',
  icon text default 'folder',
  created_at timestamptz default now(),
  updated_at timestamptz default now()
);

alter table public.projects enable row level security;

create policy "Users can view their own projects"
  on public.projects for select
  using ( auth.uid() = user_id );

create policy "Users can insert their own projects"
  on public.projects for insert
  with check ( auth.uid() = user_id );

create policy "Users can update their own projects"
  on public.projects for update
  using ( auth.uid() = user_id );

create policy "Users can delete their own projects"
  on public.projects for delete
  using ( auth.uid() = user_id );

-- =============================================
-- FILES: Track all uploaded files
-- =============================================
create table public.files (
  id uuid default uuid_generate_v4() primary key,
  user_id uuid references public.profiles(id) on delete cascade not null,
  chat_id uuid references public.chats(id) on delete cascade,
  mission_id uuid references public.missions(id) on delete cascade,
  filename text not null,
  file_type text not null,
  file_size bigint not null,
  storage_path text not null,
  mime_type text not null,
  created_at timestamptz default now()
);

alter table public.files enable row level security;

create policy "Users can view their own files"
  on public.files for select
  using ( auth.uid() = user_id );

create policy "Users can insert their own files"
  on public.files for insert
  with check ( auth.uid() = user_id );

create policy "Users can delete their own files"
  on public.files for delete
  using ( auth.uid() = user_id );
