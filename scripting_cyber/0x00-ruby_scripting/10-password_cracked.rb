require 'digest'

if ARGV.length < 2
  puts "Usage: 10-password_cracked.rb HASHED_PASSWORD DICTIONARY_FILE"
else
  hashed = ARGV[0]
  dictionary = ARGV[1]
  found = false
  File.foreach(dictionary) do |word|
    word = word.chomp
    if Digest::SHA256.hexdigest(word) == hashed
      puts "Password found: #{word}"
      found = true
      break
    end
  end
  puts "Password not found in dictionary." unless found
end
